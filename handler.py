import json


def hello(event, context):
    try:
        from packages.sample_module import GREETING
        msg = GREETING
    except:
        print('FAILED: from packages.sample_module import GREETING')
        try:
            from sample_module import GREETING
            msg = GREETING
        except:
            print('FAILED: from sample_module import GREETING')
            msg = "Go Serverless v1.0! Your function executed successfully! (almost)"
    body = {
        "message": msg,
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
