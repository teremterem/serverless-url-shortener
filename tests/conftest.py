import json
import shlex
import sys

import pytest

from tests.local_lambda import LocalLambda

sys.path.append('layer/common-code/python')


@pytest.fixture
def hello_lambda():
    return LocalLambda(
        lambda event: f'docker-compose run --rm --service-ports python3.8-lambda '
                      f'tests/mocking_handlers.mocking_hello {shlex.quote(json.dumps(event))}'
    )
