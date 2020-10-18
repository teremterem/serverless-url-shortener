import json

from sample_module import greeting, get_real

try:
    from tests.local_lambda import mockable
except ImportError:
    def mockable(func):
        return func


@mockable
def hello(event, context):
    # breakpoint()
    body = {
        "message": f'{greeting()} {get_real()}',
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
