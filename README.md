
# Serverless URL Shortener

## Debug lambdas locally

- https://github.com/ionelmc/python-remote-pdb#integration-with-breakpoint-in-python-37
- https://github.com/ionelmc/python-remote-pdb#usage

!!! To see internal lambda logs run lambda directly instead of through pytest:
```
docker-compose run --rm python3.8-lambda function/hello.hello '{}'
```

- TODO redirect stderr to some kind of pytest logger ? or simply to stderr or stdout ?
