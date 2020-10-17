
# Serverless URL Shortener

## Test lambdas locally

```
pipenv run python -m pytest
```
OR
```
pipenv run python -m pytest -svv --log-cli-level=DEBUG
```

## Debug lambdas locally

- https://github.com/ionelmc/python-remote-pdb#integration-with-breakpoint-in-python-37
- https://github.com/ionelmc/python-remote-pdb#usage

```
nc -C 127.0.0.1 4444
docker-compose run --rm python3.8-lambda function/hello.hello '{}'
```

- https://docs.docker.com/compose/reference/run/

## TODO

- Try `sls invoke local --docker` !!!
  - https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke-local/
  - what about alternative "mocking" handlers though ?
