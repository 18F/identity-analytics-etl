# identity-analytics-etl

This repository is designed to parse and migrate our logs from an s3 bucket,
into another s3 bucket with processed tabular (csv) data that gets copied into
Redshift. While, this is a work in progress, it is designed to be deployed on
AWS lambda. This will serve as the underlying ETL powering the product Analytics
for login.gov

## Developing

The repository uses `python3` and `virtualenv`

To install requirements:

```
make venv
```

To run tests:

```
make clean
```

to deploy a new lambda function to the deployments s3 bucket:

```
make lambda_deploy ENVIRONMENT="{$ENVIRONMENT_NAME}" TAG="{TAG_NUMBER}"
```

### Notes

Previously, this repository was written in [Ruby](https://github.com/18F/identity-redshift).
The motivation for rewriting is that Python can be run on Lambda while Ruby cannot.
This should run locally, so long as the postgresql server is running.
There is an open PR (#299) in identity-devops providing the terraform plans for
creating the infrastructure needed for this.
