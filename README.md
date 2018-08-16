# identity-analytics-etl

This repository is designed to parse and migrate our logs from an s3 bucket,
into another s3 bucket with processed tabular (csv) data that gets copied into
Redshift. While, this is a work in progress, it is designed to be deployed on
AWS lambda. This will serve as the underlying ETL powering the product Analytics
for login.gov

## Developing

The repository uses `python 3`, `pipenv`, and `docker`

To install pipenv:
for MacOS, you can use Homebrew
    `$ brew install pipenv `
for other OSes, follow these instructions https://docs.pipenv.org/install/#installing-pipenv

To install Docker:  
(MacOSX) https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac
(Debian) https://docs.docker.com/install/linux/docker-ce/debian/ 
(Ubuntu) https://docs.docker.com/install/linux/docker-ce/ubuntu/#os-requirements
  
To install requirements:

```
make init
```

To run tests:

```
make clean
```

To check code coverage locally:

```
make coverage
```

to deploy a new lambda function to the deployments s3 bucket:
if running for the first time:
```
make lambda_buckets ENVIRONMENT="{$ENVIRONMENT_NAME}"
```

```
make lambda_deploy TAG="{TAG_NUMBER}"
```

Then in identity-devops repository:
```
./deploy-analytics {env} apply
```

Afterwards, be sure to locate the kms key you are using and add all of the roles and user created by terraform to that key. 
