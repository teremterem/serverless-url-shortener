
# Serverless URL Shortener

## TODO

### Document

- If you use serverless plugins then document how to install them from package.json using npm (altogether instead of
  one by one).

### serverless-python-requirements plugin

- !!! https://github.com/UnitedIncome/serverless-python-requirements#optimising-packaging-time
- Use "dockerizePip: true" as default to be absolutely sure that dependencies are compiled exactly the same way on any
  deploying machine? Yes! The plugin will try to use python binary to run pipenv (and the binary situation may be
   different from OS to OS and from computer to computer).
  - Would it also be preferable to use docker to run tests then (also to be absolutely sure it behaves exactly the
    same way on any machine)?
    https://github.com/UnitedIncome/serverless-python-requirements#native-code-dependencies-during-build
  - *Why wouldn't you go as far as installing even serverless cli itself inside docker and then deploying from docker?
    (What for, though? No, please don't do this...)*
    - Here is a hint on why it may be needed:  
      https://github.com/UnitedIncome/serverless-python-requirements#customize-python-executable  
      https://github.com/UnitedIncome/serverless-python-requirements#applebeersnake-mac-brew-installed-python-notes
      (actually - it is not needed - "dockerizePip: true" is enough)
- Use "slim: true"? Once again, what for? Out of curiosity... If you are going to try it then make sure to try it
  against, for ex., numpy as a library which has its' parts written in C.

### Try out

- AWS Lambda Layer(s) for Python dependencies
  - pipenv
  - make sure layers aren't redeployed everytime lambdas are deployed (should redeploy only when changed)
  - mention env name in layer name
- GraphQL
- DynamoDB
- Cognito

---

- https://www.serverless.com/blog/stages-and-environments#separate-aws-accounts
- Additional URL Shortener requirement - preview long url page instead of following over to it. This will require
  additional libs (which will help showcase working with lambdas with various dependencies):
  - requests (to get the page without redirecting the user to it)
  - some kind of html stripping lib ? there is no need to install anything from 3rd party, though -
    https://stackoverflow.com/a/925630/2040370
  - **use NumPy for no reason?**

### Research (and document)

- Test driven development (what would be the scope of test coverage?)
  - pytest?
    - for "common-code" layer (if still relevant): https://stackoverflow.com/a/3108301/2040370
  - separate unit tests from integration tests and let integration tests hit the real deployment? (what to do about
    setup/teardown for integration tests though?)
- Debugging
- Serverless staging approach (with team work in mind)
- CI/CD (how to enforce test execution)

---

- Set up an alert for lambdas to not go over certain runtime threshold to protect from possible inadvertent
  endless recursion of lambdas (a mistake that is not that hard to make but which may cost a lot - google it)
  - FYI asynchronous invocations involve 2 retries by default in case of failure (configurable)
- Warm up lambdas? (minor... google it)

### Research (extra)

- Try deploying NumPy in a lambda layer to see how it goes with a Python+C lib?

---

- Is Async IO used somehow in Python AWS Lambdas? (Any external event loop?)
  - https://www.trek10.com/blog/aws-lambda-python-asyncio
- **Combine AWS Amplify with Serverless? (Is it still reasonable/viable to do so? The correspondent plugin repo is now
  archived for some reason...)**
  - https://www.serverless.com/plugins/aws-amplify-serverless-plugin
- Compare Serverless to AWS Amplify?
  - https://medium.com/@mim3dot/aws-amplify-pros-and-cons-bf77a98da5db

## Minor

- Mention that layer/common-code/python/ should be added to a list of source directories in IDE?
  - Do we even need common-code layer though? Why not just package py files together with lambdas that need them?
    (Source files are always lightweight - not worth the trouble of deployment separation.)

## References

- *https://guides.github.com/introduction/flow/ (see "Note of reflection" at the top of
  https://nvie.com/posts/a-successful-git-branching-model/)*
- https://medium.com/@mim3dot/dead-simple-aws-graphql-api-59db32510bfb
- https://www.serverless.com/framework/docs/providers/aws/guide/credentials/
- https://www.serverless.com/framework/docs/dashboard/access-roles/
- https://www.serverless.com/blog/publish-aws-lambda-layers-serverless-framework
- https://www.serverless.com/framework/docs/providers/aws/guide/layers/
- https://medium.com/@adhorn/getting-started-with-aws-lambda-layers-for-python-6e10b1f9a5d
- **https://www.serverless.com/plugins/serverless-python-requirements**
  - https://www.serverless.com/blog/serverless-python-packaging
  - **https://github.com/lambci/docker-lambda**
  - https://medium.com/@dorian599/serverless-aws-lambda-layers-and-python-dependencies-92741138bf31
  - **https://blog.francium.tech/deploying-python-packages-to-lambda-layers-using-serverless-plugin-c8fe1371e0b**
  - https://github.com/UnitedIncome/serverless-python-requirements/issues/485#issuecomment-594184967
    - https://github.com/UnitedIncome/serverless-python-requirements/pull/310
- https://www.serverless.com/framework/docs/providers/aws/guide/variables/
- https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html
- https://forum.serverless.com/t/package-excludes-do-not-seem-to-work/2314/5
- **https://www.serverless.com/blog/quick-tips-for-faster-serverless-development**

---

- *"Blank" python serverless app:
  https://github.com/teremterem/serverless-url-shortener/commit/4bc94725745b153c8370d4583ac148e045975e66*
