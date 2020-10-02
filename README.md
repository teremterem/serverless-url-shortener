
# Serverless URL Shortener

## Run lambda locally

```
docker-compose run --rm test-python3.8-lambdas function/hello.hello '{}'
```

## Test

Temporary:
```
pipenv run python -m pytest
```

- TODO: do ipdb right away to make your life easier ?
- https://www.serverlessops.io/blog/aws-lambda-serverless-development-workflow-part2-testing-debugging

---

- TODO: involve coverage too

## Debug

# Log into local lambda docker

- TODO? figure out how to fully emulate lambda environment using it's "bootstrap" in tests?
  - https://phoenixnap.com/kb/docker-run-override-entrypoint
  - https://github.com/lambci/docker-lambda/blob/master/python3.8/run/Dockerfile
  - https://neuvector.com/cloud-security/how-aws-lambda-serverless-works/


Log in and see bootstrap.py:
```
docker-compose run --rm --entrypoint /bin/bash test-python3.8-lambdas
cat /var/runtime/bootstrap.py
```

## Resources

- https://github.com/lambci/docker-lambda
- https://runnable.com/docker/advanced-docker-compose-configuration
- https://nickjanetakis.com/blog/a-docker-compose-override-file-can-help-avoid-compose-file-duplication
  - TODO: https://www.youtube.com/watch?v=jGePPQFArwo
- https://stackoverflow.com/a/42260979/2040370
- https://docs.docker.com/docker-for-mac/osxfs-caching/
- https://stackoverflow.com/a/49985823/2040370
- https://stackoverflow.com/a/61218274/2040370
- https://docs.docker.com/develop/develop-images/multistage-build/
- https://docs.pytest.org/en/stable/goodpractices.html#tests-outside-application-code
  - https://docs.pytest.org/en/stable/pythonpath.html#pytest-vs-python-m-pytest

---

- https://stackoverflow.com/a/62967574/2040370
