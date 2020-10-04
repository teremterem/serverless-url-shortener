
# Serverless URL Shortener

## Run lambda locally

```
docker-compose run --rm python3.8-lambda function/hello.hello '{}'
```

- **https://levelup.gitconnected.com/aws-lambda-offline-development-with-docker-6a8cf8b186e7**
  - **https://github.com/vittorio-nardone/aws-lambda-offline-development/blob/master/Makefile**
- https://blog.thundra.io/is-it-possible-to-debug-lambdas-locally
- https://stackoverflow.com/questions/45928842/multiple-volumes-to-single-target-directory

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

- !!!!!!!!!! https://github.com/ionelmc/python-remote-pdb
- https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-automated-tests.html
- https://sanderknape.com/2018/02/comparing-aws-sam-with-serverless-framework/
- https://github.com/pypa/pipenv/issues/2206
  - https://github.com/pypa/pipenv/issues/746

# Log into local lambda docker

- TODO? figure out how to fully emulate lambda environment using it's "bootstrap" in tests?
  - https://phoenixnap.com/kb/docker-run-override-entrypoint
  - https://github.com/lambci/docker-lambda/blob/master/python3.8/run/Dockerfile
  - https://neuvector.com/cloud-security/how-aws-lambda-serverless-works/


Log in and see bootstrap.py:
```
docker-compose run --rm --entrypoint /bin/bash python3.8-lambda
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
- give AWS SAM a shot?
  - https://medium.com/better-programming/how-to-deploy-a-local-serverless-application-with-aws-sam-b7b314c3048c
