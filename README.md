
# Serverless URL Shortener

## Debug lambdas locally

- https://github.com/ionelmc/python-remote-pdb#integration-with-breakpoint-in-python-37
- https://github.com/ionelmc/python-remote-pdb#usage

!!! To see internal lambda logs run lambda directly instead of through pytest:
```
docker-compose run --rm python3.8-lambda function/hello.hello '{}'
```

- https://stackoverflow.com/a/58630093/2040370
- https://docs.docker.com/compose/compose-file/#network_mode
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-debugging-python.html#serverless-sam-cli-using-debugging-python-ptvsd
