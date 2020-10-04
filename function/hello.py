import json

from sample_module import GREETING


def hello(event, context):
    # breakpoint()
    from remote_pdb import RemotePdb
    RemotePdb('127.0.0.1', 4444).set_trace()
    body = {
        "message": GREETING,
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
