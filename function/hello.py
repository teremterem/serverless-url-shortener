import json

from sample_module import GREETING, get_real


def hello(event, context):
    # breakpoint()
    body = {
        "message": GREETING + ' ' + get_real(),
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
