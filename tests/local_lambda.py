import json
import logging
import os
import subprocess
from contextlib import contextmanager
from functools import wraps
from importlib import import_module
from pprint import pformat

logger = logging.getLogger(__name__)

LOCAL_LAMBDA_MOCKER_ENV_VAR = '_LOCAL_LAMBDA_MOCKER'

_JSON_IN_HTTP_BODY_DEFAULT = True
_EXPECTED_EXIT_CODE_DEFAULT = 0
_MOCKABLE_LOG_LEVEL = logging.WARNING


def mockable(func):
    # TODO how to make sure this decorator is not deployed to remote lambda at all ?
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.log(_MOCKABLE_LOG_LEVEL, '@mockable: entering %r', func)
        mocker_str = os.environ.get(LOCAL_LAMBDA_MOCKER_ENV_VAR)
        if mocker_str:
            logger.log(_MOCKABLE_LOG_LEVEL, '@mockable: mocker_str=%r', mocker_str)

            mocker_module_name, mocker_name = mocker_str.split('::', maxsplit=2)
            mocker_module = import_module(mocker_module_name, package='.')
            mocker = getattr(mocker_module, mocker_name)

            logger.log(_MOCKABLE_LOG_LEVEL, '@mockable: using mocker %r', mocker)
            return mocker(func, *args, **kwargs)

        logger.log(_MOCKABLE_LOG_LEVEL, '@mockable: none or empty mocker_str')
        return func(*args, **kwargs)

    return wrapper


class LocalLambda:
    def __init__(self, shell_command_builder):
        self.shell_command_builder = shell_command_builder

    def invoke(self, event, mocker_str=None, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT,
               json_in_http_body=_JSON_IN_HTTP_BODY_DEFAULT):
        return self.invoker(
            event, mocker_str=mocker_str, expected_exit_code=expected_exit_code
        ).invoke(json_in_http_body=json_in_http_body)

    def invoke_plain(self, event, mocker_str=None, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT):
        return self.invoker(
            event, mocker_str=mocker_str, expected_exit_code=expected_exit_code
        ).invoke_plain()

    def invoker(self, event, mocker_str=None, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT):
        return _LocalLambdaInvoker(self, event, mocker_str, expected_exit_code)


def fix_json_in_body(lambda_response_json):
    body = lambda_response_json.get('body')
    if body:
        lambda_response_json['body'] = json.loads(body)
    return lambda_response_json


class LocalLambdaInvoker:
    def __init__(self, local_lambda, event, mocker_str, expected_exit_code):
        self.local_lambda = local_lambda
        self.event = event
        self.expected_exit_code = expected_exit_code

        self.shell_command = self.local_lambda.shell_command_builder(event, mocker_str)

    def invoke(self, json_in_http_body=_JSON_IN_HTTP_BODY_DEFAULT):
        output_json = json.loads(self.invoke_plain())
        # TODO include original stdout into exception message if json parsing fails (use exception chaining?)

        json_in_http_body_exc = False
        if json_in_http_body:
            try:
                # assume it is an http lambda that returns json in its response body
                fix_json_in_body(output_json)
            except (TypeError, ValueError) as e:
                # no, it is not... but that's fine too!
                json_in_http_body_exc = e

        output_json_message = (
            'OUTPUT JSON\n'
            '%(output_json)s\n'
            'END OUTPUT JSON\n'
        )
        if json_in_http_body_exc:
            if logger.isEnabledFor(logging.WARNING):
                logger.warning(
                    'Failed to parse body of http lambda response as json. To get rid of this warning (if it is not an '
                    'http lambda or its response body is not supposed to be json) set json_in_http_body to False.' +
                    self._LAMBDA_RUN_MESSAGE +
                    output_json_message,
                    {
                        'shell_command': self.shell_command,
                        'output_json': pformat(output_json),
                        'exc_info': json_in_http_body_exc,
                    },
                )
        elif logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                self._LAMBDA_RUN_MESSAGE +
                output_json_message,
                {
                    'shell_command': self.shell_command,
                    'output_json': pformat(output_json),
                },
            )

        return output_json

    def invoke_plain(self):
        with self._spawn_docker_service() as lambda_output:
            output_bytes = lambda_output.read()

        logger.debug(
            self._LAMBDA_RUN_MESSAGE +
            'OUTPUT\n'
            '%(output_bytes)s\n'
            'END OUTPUT\n',
            {
                'shell_command': self.shell_command,
                'output_bytes': output_bytes,
            },
        )
        return output_bytes

    @contextmanager
    def _spawn_docker_service(self):
        logger.debug(
            self._LAMBDA_RUN_MESSAGE +
            'BEGIN\n',
            {
                'shell_command': self.shell_command,
            },
        )

        subproc = subprocess.Popen(
            self.shell_command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:  # https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
            yield subproc.stdout
        finally:
            subproc.stdout.close()

            exit_code = subproc.wait()
            if self.expected_exit_code is not None and exit_code != self.expected_exit_code:
                raise AssertionError(
                    (
                            'ACTUAL EXIT CODE (%(actual_exit_code)s) != EXPECTED EXIT CODE (%(expected_exit_code)s)' +
                            self._LAMBDA_RUN_MESSAGE +
                            '\n'
                            'CHECK LAMBDA\'S STDERR TO SEE WHAT THE PROBLEM IS.\n'
                            '\n'
                            '(NOTE: If, for any reason, you need to disable this assertion completely, pass '
                            'expected_exit_code=None)'
                    ) % {
                        'shell_command': self.shell_command,
                        'expected_exit_code': self.expected_exit_code,
                        'actual_exit_code': exit_code,
                    },
                )

            if self.expected_exit_code is None and exit_code != 0:
                log_level = logging.WARNING
            else:
                log_level = logging.DEBUG

            logger.log(
                log_level,
                self._LAMBDA_RUN_MESSAGE +
                'EXIT CODE: %(exit_code)s\n',
                {
                    'shell_command': self.shell_command,
                    'exit_code': exit_code,
                },
            )

    _LAMBDA_RUN_MESSAGE = (
        '\n'
        '\n'
        'LOCAL LAMBDA RUN\n'
        '%(shell_command)s\n'
    )


_LocalLambdaInvoker = LocalLambdaInvoker
