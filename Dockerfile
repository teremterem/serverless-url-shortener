# https://github.com/lambci/docker-lambda
FROM lambci/lambda:python3.8

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
# https://github.com/awslabs/amazon-sagemaker-examples/issues/319
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile /code/
COPY Pipfile.lock /code/

RUN pip install pipenv==2020.8.13
RUN pipenv install --dev --deploy

COPY . /code/
