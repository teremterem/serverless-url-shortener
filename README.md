
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
docker-compose run --rm python3.8-lambda function/hello.hello '{}'
```

- https://docs.docker.com/compose/reference/run/
