Redshift is a postgres-like database. But uniqueness, primary key, and foreign key constraints are informational only; they are not enforced by Amazon Redshift. See https://docs.aws.amazon.com/redshift/latest/dg/t_Defining_constraints.html.

This directory has some SQL queries to help you explore the duplicate data.

Impact of duplicates in event data:

1. We have to use expensive ``DISTINCT`` or ``GROUP BY`` operation in queries, which makes our query over complicate.
2. It leads to inaccurate value and sometimes hard to be aware.
3. For user log in attempts relative analysis, duplicate data is a disaster.
