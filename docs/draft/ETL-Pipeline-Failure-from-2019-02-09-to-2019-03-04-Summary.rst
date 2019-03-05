ETL Pipeline Failure from 2019-02-09 to 2019-03-04 Summary
==============================================================================


Description
------------------------------------------------------------------------------
Redshift stopped receiving any data from 2019-02-09.

The Logstash data are correctly parsed and sitting in Hot Bucket, but data are not correctly loaded to Redshift

Reason Investigation
------------------------------------------------------------------------------

Lambda make S3 API call to get list of CSV file, and filter out those already done. But around 2019-02-09, too much files are uploaded to Hot Bucket, which causes the S3 API call timed out.


Solution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since files are immediately deleted from Hot bucket, we are actually using s3 like Task Queue, we should limit number of task to retrieve in S3 API call instead of retrieve all of them.


Current Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Patched codes are deployed, now we overstocked **450,000 files**. I can visually see that number of rows data are growing after I fixed it. The rate is like 250 files per 5 min, it takes **450,000 / 250 x 5 / 60 = 150 Hour** to repopulate everything.

I changed the cron job from 5 min to 1 min, and will change it back once all data are re-uploaded. Approximately it takes **150 / 5 = 30 Hour**
