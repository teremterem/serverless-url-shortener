import json
import logging
import os
import shlex

import pytest

from function.hello import hello

logger = logging.getLogger(__name__)


# TODO either use skipif (if possible) or a custom mark to separate between unit and integration tests
#  https://docs.pytest.org/en/stable/mark.html
#  or separate unit and integration tests in some other way ?
@pytest.mark.skip
def test_hello_inside():
    result = hello({}, None)
    # TODO use labci to emulate context ?
    assert result == {'body': '{"message": "GREETING from Lambda Layer!", "input": {}}', 'statusCode': 200}


def invoke_lambda_plain(handler, event):
    with os.popen(
            f'docker-compose run --rm python3.8-lambda {handler} {shlex.quote(json.dumps(event))}'
    ) as response:
        return json.load(response)


def invoke_lambda(handler, event):
    response = invoke_lambda_plain(handler, event)
    if 'body' in response:
        try:
            # assume it is an http lambda that returns json in its response body
            response['body'] = json.loads(response['body'])
        except (TypeError, ValueError):
            # no, it is not... but that's fine too!
            logger.debug('Failed to parse body of http lambda response as json', exc_info=True)
    return response


def test_hello():
    assert invoke_lambda('function/hello.hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'GREETING from Lambda Layer!'}, 'statusCode': 200}
