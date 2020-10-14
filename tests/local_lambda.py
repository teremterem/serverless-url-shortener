import json
import logging
import shlex
import subprocess
from contextlib import contextmanager
from pprint import pformat

logger = logging.getLogger(__name__)


class LocalLambda:
    def __init__(self, docker_compose_service):
        self.docker_compose_service = docker_compose_service

    def invoke(self, handler, event, expected_exit_code=0):
        response = invoke_lambda_plain(handler, event)
        if 'body' in response:
            try:
                # assume it is an http lambda that returns json in its response body
                response['body'] = json.loads(response['body'])
            except (TypeError, ValueError):
                # no, it is not... but that's fine too!
                logger.warning(
                    'Failed to parse body of http lambda response as json. If this is not an http lambda then you can get '
                    'rid of this warning by using invoke_plain() instead of invoke().',
                    exc_info=True,
                )
        return response


class LocalLambdaInvoker:
    def __init__(self, local_lambda, handler, event, json_in_http_body, expected_exit_code):
        self.local_lambda = local_lambda
        self.handler = handler
        self.event = event
        self.json_in_http_body = json_in_http_body
        self.expected_exit_code = expected_exit_code

        self.shell_command = self._build_shell_command()
        self._lambda_run_message = (
            '\n'
            '\n'
            'LOCAL LAMBDA RUN\n'
            '{shell_command}\n'
        )

    def invoke(self):
        output_json = json.loads(self.invoke_plain())

        json_in_http_body_exc = False
        if self.json_in_http_body and 'body' in output_json:
            try:
                # assume it is an http lambda that returns json in its response body
                output_json['body'] = json.loads(output_json['body'])
            except (TypeError, ValueError) as e:
                # no, it is not... but that's fine too!
                json_in_http_body_exc = e

        output_json_message = (
            'OUTPUT JSON\n'
            '{output_json}\n'
            'END OUTPUT JSON\n'
        )
        if json_in_http_body_exc:
            if logger.isEnabledFor(logging.WARNING):
                logger.warning(
                    'Failed to parse body of http lambda response as json. To get rid of this warning (if it is not an '
                    'http lambda or its response body is not supposed to be json) set json_in_http_body to False.' +
                    self._lambda_run_message +
                    output_json_message,
                    shell_command=self.shell_command,
                    output_json=pformat(output_json),
                    exc_info=json_in_http_body_exc,
                )
        elif logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                self._lambda_run_message +
                output_json_message,
                shell_command=self.shell_command,
                output_json=pformat(output_json)
            )

        return output_json

    def invoke_plain(self):
        with self._spawn_docker_service() as lambda_output:
            output_bytes = lambda_output.read()

            logger.debug(
                self._lambda_run_message +
                'OUTPUT\n'
                '{output_bytes}\n'
                'END OUTPUT\n',
                shell_command=self.shell_command,
                output_bytes=pformat(output_bytes)
            )
            return output_bytes

    def _build_shell_command(self):
        return f'docker-compose run --rm --service-ports {self.local_lambda.docker_compose_service} ' \
               f'{self.handler} {shlex.quote(json.dumps(self.event))}'

    @contextmanager
    def _spawn_docker_service(self):
        logger.debug(
            self._lambda_run_message +
            'BEGIN\n',
            shell_command=self.shell_command,
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
                raise AssertionError((
                        self._lambda_run_message +
                        'EXPECTED EXIT CODE: {expected_exit_code}\n' +
                        'ACTUAL EXIT CODE: {actual_exit_code}\n' +
                        '(NOTE: to turn off this assertion set expected_exit_code to None)\n'
                ).format(
                    shell_command=self.shell_command,
                    expected_exit_code=self.expected_exit_code,
                    actual_exit_code=exit_code,
                ))
            logger.debug(
                self._lambda_run_message +
                'EXIT CODE: {exit_code}\n',
                shell_command=self.shell_command,
                exit_conde=exit_code,
            )


_LocalLambdaInvoker = LocalLambdaInvoker
