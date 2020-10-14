import json
import logging
import shlex
import subprocess
from contextlib import contextmanager

from function.hello import hello

logger = logging.getLogger(__name__)


def test_hello_inside():
    result = hello({}, None)
    assert result == {'body': '{"message": "GREETING from Lambda Layer! REAL", "input": {}}', 'statusCode': 200}


def invoke_lambda_plain(handler, event):
    # TODO turn it into an object instantiated by a fixture -
    #  this way it will be easy to make it configurable/reusable
    @contextmanager
    def _spawn_lambda():
        command = f'docker-compose run --rm --service-ports python3.8-lambda ' \
                  f'{handler} {shlex.quote(json.dumps(event))}'
        logger.debug(
            '\n'
            '\n'
            'LOCAL LAMBDA RUN\n'
            '%s\n'
            'BEGIN\n',
            command,
        )

        subproc = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:  # https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
            yield subproc.stdout, command
        finally:
            subproc.stdout.close()

            exit_code = subproc.wait()
            # TODO make expected exit code configurable and throw AssertionError from here if it is not met
            logger.log(
                logging.DEBUG if exit_code == 0 else logging.ERROR,
                '\n'
                '\n'
                'LOCAL LAMBDA RUN\n'
                '%s\n'
                'EXIT CODE: %s\n',
                command,
                exit_code,
            )

    with _spawn_lambda() as (lambda_output, command):
        output_bytes = lambda_output.read()

        logger.debug(
            '\n'
            '\n'
            'LOCAL LAMBDA RUN\n'
            '%s\n'
            'OUTPUT\n'
            '%s\n'
            'END OUTPUT\n',
            command,
            output_bytes,  # TODO how to present it ? pformat of already parsed json ?
        )
    return json.loads(output_bytes)


def invoke_lambda(handler, event):
    response = invoke_lambda_plain(handler, event)
    if 'body' in response:
        try:
            # assume it is an http lambda that returns json in its response body
            response['body'] = json.loads(response['body'])
        except (TypeError, ValueError):
            # no, it is not... but that's fine too!
            logger.warning(
                'Failed to parse body of http lambda response as json. If this is not an http lambda then you can get '
                'rid of this warning by using invoke_lambda_plain() instead of invoke_lambda().',
                exc_info=True,
            )
    return response


def test_hello():
    assert invoke_lambda('tests/mocking_handlers.mocking_hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}
