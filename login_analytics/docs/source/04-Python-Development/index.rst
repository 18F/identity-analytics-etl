Python Development
==============================================================================


1. How to manage python code.
------------------------------------------------------------------------------

- the python library should be installable and importable.
- write doc string and test.


2. How to manage lambda code.
------------------------------------------------------------------------------

- Lambda Function should have version.
- AWS API Logic should be separate from the core logic, such as ETL logic.
- Handler should be able to test locally.


3. How to devops lambda functions
------------------------------------------------------------------------------

- temp solution: make file
- long term solution: use management tools, serverless, https://serverless.com/framework/docs/providers/aws/guide/functions/


4. How to manage local and cloud environment.
------------------------------------------------------------------------------

Leave as it is.

- makefile + shell scripts + terraform.


5. How to manage analytics query / scripts.
------------------------------------------------------------------------------

- SQL: dev it in doc source
- Analytics Python Scripts: dev it in python library


6. How to manage docs.
------------------------------------------------------------------------------

- Write doc at where you need it, for example, if you are writing doc for your code, write it in your code or near your code.


7. How to add new feature.
------------------------------------------------------------------------------

feature branch workflow: https://www.atlassian.com/git/tutorials/comparing-workflows

- dev new feature
- add test
- run test
- PR
- code review
- approve


