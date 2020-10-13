import json
import logging
import shlex
import subprocess
from contextlib import contextmanager

from function.hello import hello

logger = logging.getLogger(__name__)


# TODO either use skipif (if possible) or a custom mark to separate between unit and integration tests
#  https://docs.pytest.org/en/stable/mark.html
#  or separate unit and integration tests in some other way ?
def test_hello_inside():
    result = hello({}, None)
    assert result == {'body': '{"message": "GREETING from Lambda Layer! REAL", "input": {}}', 'statusCode': 200}


def invoke_lambda_plain(handler, event):
    @contextmanager
    def _spawn_lambda():
        command = f'docker-compose run --rm --service-ports python3.8-lambda ' \
                  f'{handler} {shlex.quote(json.dumps(event))}'
        logger.info(
            '\n'
            '\n'
            'LOCAL LAMBDA RUN\n'
            '%s\n'
            'BEGIN\n',
            command,
        )

        subp = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        try:  # https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
            yield subp.stdout
        finally:
            subp.stdout.close()
            exit_code = subp.wait()
            logger.log(
                logging.INFO if exit_code == 0 else logging.ERROR,
                '\n'
                '\n'
                'LOCAL LAMBDA RUN\n'
                '%s\n'
                'EXIT CODE: %s\n',
                command,
                exit_code,
            )

    with _spawn_lambda() as lambda_output:
        return json.load(lambda_output)


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


# @pytest.mark.skip
def test_hello():
    assert invoke_lambda('tests/mocking_handlers.mocking_hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}
