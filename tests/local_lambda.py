import json
import logging
import subprocess
from contextlib import contextmanager
from functools import wraps
from pprint import pformat

logger = logging.getLogger(__name__)

_JSON_IN_HTTP_BODY_DEFAULT = True
_EXPECTED_EXIT_CODE_DEFAULT = None


def mockable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO
        return func(*args, **kwargs)

    return wrapper


class LocalLambda:
    def __init__(self, shell_command_builder):
        self.shell_command_builder = shell_command_builder

    def invoke(self, event, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT,
               json_in_http_body=_JSON_IN_HTTP_BODY_DEFAULT):
        return self.invoker(event, expected_exit_code=expected_exit_code).invoke(json_in_http_body=json_in_http_body)

    def invoke_plain(self, event, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT):
        return self.invoker(event, expected_exit_code=expected_exit_code).invoke_plain()

    def invoker(self, event, expected_exit_code=_EXPECTED_EXIT_CODE_DEFAULT):
        return _LocalLambdaInvoker(self, event, expected_exit_code)


def fix_json_in_body(lambda_response_json):
    body = lambda_response_json.get('body')
    if body:
        lambda_response_json['body'] = json.loads(body)
    return lambda_response_json


class LocalLambdaInvoker:
    def __init__(self, local_lambda, event, expected_exit_code):
        self.local_lambda = local_lambda
        self.event = event
        self.expected_exit_code = expected_exit_code

        self.shell_command = self.local_lambda.shell_command_builder(event)

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
                    }
                )
        elif logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                self._LAMBDA_RUN_MESSAGE +
                output_json_message,
                {
                    'shell_command': self.shell_command,
                    'output_json': pformat(output_json),
                }
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
            }
        )
        return output_bytes

    @contextmanager
    def _spawn_docker_service(self):
        logger.debug(
            self._LAMBDA_RUN_MESSAGE +
            'BEGIN\n',
            {
                'shell_command': self.shell_command,
            }
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
                            self._LAMBDA_RUN_MESSAGE
                    ) % {
                        'shell_command': self.shell_command,
                        'expected_exit_code': self.expected_exit_code,
                        'actual_exit_code': exit_code,
                    }
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
                }
            )

    _LAMBDA_RUN_MESSAGE = (
        '\n'
        '\n'
        'LOCAL LAMBDA RUN\n'
        '%(shell_command)s\n'
    )


_LocalLambdaInvoker = LocalLambdaInvoker
