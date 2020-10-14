import logging

from function.hello import hello

logger = logging.getLogger(__name__)


def test_hello_inside():
    result = hello({}, None)
    assert result == {'body': '{"message": "GREETING from Lambda Layer! REAL", "input": {}}', 'statusCode': 200}


def test_hello():
    assert invoke_lambda('tests/mocking_handlers.mocking_hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}
