from function.hello import hello
from tests.local_lambda import fix_json_in_body


def test_hello_inside():
    result = fix_json_in_body(hello({}, None))
    assert result == {'body': {'input': {}, 'message': 'GREETING from Lambda Layer! REAL'}, 'statusCode': 200}


def test_hello_no_mocker(hello_lambda):
    result = hello_lambda.invoke({'a': ['b']})
    assert result == {'body': {'input': {'a': ['b']}, 'message': 'GREETING from Lambda Layer! REAL'}, 'statusCode': 200}


def test_hello(hello_lambda):
    result = hello_lambda.invoke({'a': ['b']}, mocker_str='tra.ta::ta')
    assert result == {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}
