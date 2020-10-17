import json
import shlex
import sys

import pytest

from tests.local_lambda import LocalLambda, LOCAL_LAMBDA_MOCKER_ENV_VAR

sys.path.append('layer/common-code/python')


@pytest.fixture
def hello_lambda():
    return LocalLambda(
        # TODO put some version of this into the lib as reference
        lambda event, mocker_str: f'docker-compose run --rm --service-ports -e '
                                  f'{LOCAL_LAMBDA_MOCKER_ENV_VAR}={shlex.quote(mocker_str)} '
                                  f'python3.8-lambda function/hello.hello {shlex.quote(json.dumps(event))}'
    )
