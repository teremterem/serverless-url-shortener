import json
import logging
import shlex
import subprocess
import traceback
from contextlib import contextmanager

import pytest

from function.hello import hello


# TODO either use skipif (if possible) or a custom mark to separate between unit and integration tests
#  https://docs.pytest.org/en/stable/mark.html
#  or separate unit and integration tests in some other way ?
@pytest.mark.skip
def test_hello_inside():
    result = hello({}, None)
    assert result == {'body': '{"message": "GREETING from Lambda Layer!", "input": {}}', 'statusCode': 200}


def invoke_lambda_plain(handler, event):
    @contextmanager
    def _spawn_lambda():
        command = f'docker-compose run --rm python3.8-lambda {handler} {shlex.quote(json.dumps(event))}'

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
            print(f'\n{command}\nEXIT CODE: {exit_code}\n')

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
            print('WARNING! Failed to parse body of http lambda response as json', exc_info=True)
            traceback.print_exc()
    return response


# @pytest.mark.skip
def test_hello():
    assert invoke_lambda('function/hello.hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'GREETING from Lambda Layer!'}, 'statusCode': 200}
