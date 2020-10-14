import sys

import pytest

from tests.local_lambda import LocalLambda

# TODO get rid of this when docker-lambda is setup properly
sys.path.append('layer/common-code/python')


@pytest.fixture
def py38lambda():
    return LocalLambda('python3.8-lambda')
