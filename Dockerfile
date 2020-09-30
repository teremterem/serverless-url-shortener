# https://github.com/lambci/docker-lambda
FROM lambci/lambda:python3.8

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
# https://github.com/awslabs/amazon-sagemaker-examples/issues/319
ENV PYTHONUNBUFFERED 1

RUN pip install pipenv==2020.8.13

# https://github.com/lambci/docker-lambda#running-lambda-functions
WORKDIR /var/task/

COPY Pipfile /var/task/
COPY Pipfile.lock /var/task/

RUN pipenv install --dev --deploy
# TODO
#  Should I figure how to mount layer built with serverless-python-requerements plugin to /opt instead of installing
#  dependencies with pipenv right here?
#  Alternatively, you can use pipenv -t to target the installation to /opt (or to /opt/python ?)

COPY . /var/task/
