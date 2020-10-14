from function.hello import hello
from tests.local_lambda import fix_json_in_body


def test_hello_inside():
    result = fix_json_in_body(hello({}, None))
    assert result == {'body': '{"message": "GREETING from Lambda Layer! REAL", "input": {}}', 'statusCode': 200}


def test_hello(py38lambda):
    assert py38lambda.invoke('tests/mocking_handlers.mocking_hello', {'a': ['b']}) == \
           {'body': {'input': {'a': ['b']}, 'message': 'aloha fake'}, 'statusCode': 200}
