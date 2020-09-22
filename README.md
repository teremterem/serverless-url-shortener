
# Serverless URL Shortener

## TODO

### Try out

- AWS Lambda Layer(s) for Python dependencies
  - pipenv
- GraphQL
- DynamoDB
- Cognito

### Research (and document)

- Test driven development (what would be the scope of test coverage?)
  - pytest?
- Debugging
- Serverless staging approach (with team work in mind)
- CI/CD (how to enforce test execution)

---

- set up an alert for lambdas to not go over certain runtime threshold to protect from possible inadvertent
  endless recursion of lambdas (a mistake that is not that hard to make but which may cost a lot - google it)
- warm up lambdas? (minor... google it)

### Research (extra)

- Is Async IO used somehow in Python AWS Lambdas? (Any external event loop?)
- **Combine AWS Amplify with Serverless? (Is it still reasonable/viable to do so? The correspondent plugin repo is now
  archived for some reason...)**
  - https://www.serverless.com/plugins/aws-amplify-serverless-plugin
- Compare Serverless to AWS Amplify?
  - https://medium.com/@mim3dot/aws-amplify-pros-and-cons-bf77a98da5db

## References

- https://medium.com/@mim3dot/dead-simple-aws-graphql-api-59db32510bfb
- https://www.serverless.com/framework/docs/providers/aws/guide/credentials/
- https://www.serverless.com/framework/docs/dashboard/access-roles/
