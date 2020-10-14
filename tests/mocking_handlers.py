from unittest.mock import patch

from function.hello import hello


# TODO integrate this into LocalLambdaInvoker somehow
def mocking_hello(event, context):
    with patch('function.hello.get_real', return_value='fake') as mock_get_real, \
            patch('function.hello.greeting', return_value='aloha') as mock_greeting:
        # https://stackoverflow.com/a/30799104/2040370
        return hello(event, context)
