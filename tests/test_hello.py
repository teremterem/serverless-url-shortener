from unittest.mock import patch

from function.hello import hello
from tests.local_lambda import fix_json_in_body


def test_hello_inside():
    result = fix_json_in_body(hello({}, None))
    assert result == {'body': {'input': {}, 'message': 'GREETING from Lambda Layer! REAL'}, 'statusCode': 200}


def test_hello_no_mocker(hello_lambda):
    result = hello_lambda.invoke({'a': ['b']})
    assert result == {'body': {'input': {'a': ['b']}, 'message': 'GREETING from Lambda Layer! REAL'}, 'statusCode': 200}


def test_hello(hello_lambda):
    result = hello_lambda.invoke({'a': ['b']}, mocker_str='tests.test_hello::hello_mocker')
    assert result == {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}


@patch('function.hello.get_real')  # , return_value='fake')
@patch('function.hello.greeting')  # , return_value='aloha')
def hello_mocker(handler, event, context, mock_greeting, mock_get_real):
    mock_get_real.return_value = 'fake'
    mock_greeting.return_value = 'aloha'
    return handler(event, context)
