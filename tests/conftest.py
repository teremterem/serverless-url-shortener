import json
import shlex
import sys

import pytest

from tests.local_lambda import LocalLambda, LOCAL_LAMBDA_MOCKER_ENV_VAR

sys.path.append('layer/common-code/python')


@pytest.fixture
def hello_lambda():
    return _sls_invoke_local_docker('hello')


def _sls_invoke_local_docker(lambda_name):
    # TODO put some version of this function into local_lambda lib for reference
    return LocalLambda(
        lambda event, mocker_str: (
            f'serverless invoke local --function {shlex.quote(lambda_name)} --docker --skip-package '
            f'--docker-arg "-e {LOCAL_LAMBDA_MOCKER_ENV_VAR}={shlex.quote(mocker_str)}" '
            f'--docker-arg "-e PYTHONBREAKPOINT=remote_pdb.set_trace" '
            f'--docker-arg "-e REMOTE_PDB_HOST=0.0.0.0" '
            f'--docker-arg "-e REMOTE_PDB_PORT=4444" '
            f'--docker-arg "-p 4444:4444" '
            f'--data {shlex.quote(json.dumps(event))}'
        )
    )
