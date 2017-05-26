This repository is designed to parse and migrate our logs from an s3 bucket,
into another s3 bucket with processed tabular (csv) data that gets copied into
Redshift. While, this is a work in progress, it is designed to be deployed on
AWS lambda. This will serve as the underlying ETL powering the product Analytics
for login.gov


Previously, this repository was written in [Ruby](https://github.com/18F/identity-redshift).
The motivation for rewriting is that Python can be run on Lambda while Ruby cannot.
This should run locally, so long as the postgresql server is running.
There is an open PR (#299) in identity-devops providing the terraform plans for
creating the infrastructure needed for this.

For running locally do:
`$ pip install -r requirements.txt`
`$ python src/uploader.py`


 ### Architecture

 ```
 src
├── __init__.py
├── database_connection.py
├── event_parser.py
├── pageview_parser.py
├── queries.py
└── uploader.py
```

The queries creating and destroying the database as well as handling the ETL operations
exist in queries.py. All of the work in the database is led by database_connection.py.
The parsing of the logs is divided out by log type and handled by event_parser.py
and pageview_parser.py. The main script leading the work is uploader.py.

### WIP
1. Add Unit Tests (In-Progress)
2. Package Lambda function into .zip
3. Make plan for migrating/backing-up Redshift Database
4. Add better more verbose logging?
5. Use dates in s3 log names to limit lookback-range on inserts, for efficiency
6. Create s3 bucket for storing lambda function deployments, to be referenced in Terraform plans
