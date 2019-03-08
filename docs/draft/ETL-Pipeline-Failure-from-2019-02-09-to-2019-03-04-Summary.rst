ETL Pipeline Failure from 2019-02-09 to 2019-03-04 Summary
==============================================================================


Description
------------------------------------------------------------------------------
Redshift stopped receiving any data from 2019-02-09.

The Logstash data are correctly parsed and sitting in Hot Bucket, but data are not correctly loaded to Redshift.


Reason Investigation
------------------------------------------------------------------------------

We have a table ``uploaded_files`` in redshift working as duplicate filter. Lambda makes S3 API call to get list of CSV file, and filter out those already done from ``uploaded_files`` table. But around 2019-02-09, too many files are uploaded to Hot Bucket, which causes the S3 API call for getting list of CSV files to time out.


Solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since files are immediately deleted from Hot bucket after the data has been loaded to Redshift. We actually use the Hot Bucket as a fake ``Task Queue``. But it is still possible to having large number of files in the Hot Bucket. We should limit number of files to retrieve from S3 in API Call.
1000 is a good number.


Current Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The patch code is deployed, now we overstocked **450,000 files**. I can visually see that number of rows data are growing after I fixed it. The rate is like 250 files per 5 min, it takes **450,000 / 250 x 5 / 60 = 150 Hour** to repopulate everything.

I changed the cron job from 5 min to 1 min, and will change it back once all data are re-uploaded. Approximately it takes **150 / 5 = 30 Hour**
