
# Serverless URL Shortener

## TODO

### Try out

- AWS Lambda Layer(s) for Python dependencies
  - pipenv
  - make sure layers aren't redeployed everytime lambdas are deployed (should redeploy only when changed)
- GraphQL
- DynamoDB
- Cognito

### Research (and document)

- Test driven development (what would be the scope of test coverage?)
  - pytest?
  - separate unit tests from integration tests and let integration tests hit the real deployment? (what to do about
    setup/teardown for integration tests though?)
- Debugging
- Serverless staging approach (with team work in mind)
- CI/CD (how to enforce test execution)

---

- Set up an alert for lambdas to not go over certain runtime threshold to protect from possible inadvertent
  endless recursion of lambdas (a mistake that is not that hard to make but which may cost a lot - google it)
- Warm up lambdas? (minor... google it)

### Research (extra)

- Deploy only what needs to be deployed with lambda (use include/exclude directives in serverless.yml)

---

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
- https://www.serverless.com/blog/publish-aws-lambda-layers-serverless-framework
- https://www.serverless.com/framework/docs/providers/aws/guide/layers/
- https://medium.com/@adhorn/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d
