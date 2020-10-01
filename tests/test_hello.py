from function.hello import hello


def test_hello():
    result = hello({}, None)
    # TODO use labci to emulate context ?
    assert result == {'body': '{"message": "GREETING from Lambda Layer!", "input": {}}', 'statusCode': 200}
