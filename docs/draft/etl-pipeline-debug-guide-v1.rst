ETL Pipeline Debug Guide V1
==============================================================================


Check Status of the Pipeline
------------------------------------------------------------------------------


Do we have data in Redshift?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This sql scripts gives you counts of rows we copied every days. You can visually check if there is missing data. If you observed significant drop in any date, it means that **ETL Pipeline is having problems.**

.. code-block:: SQL

    \set start_time '''2018-09-01'''

    SELECT
        EVENTS.day,
        EVENTS.events_count as events_count,
        EVENTS_EMAIL.events_email_count as events_email_count,
        EVENTS_PHONE.events_phone_count as events_phone_count,
        EVENTS_DEVICES.events_devices_count as events_devices_count,
        PAGEVIEWS.pageviews_count as pageviews_count
    FROM
    (
        SELECT
            date_trunc('day', E.time) as day,
            COUNT(*) as events_count
        FROM events as E
        WHERE time >= :start_time
        GROUP BY day
    ) EVENTS
    LEFT JOIN
    (
        SELECT
            date_trunc('day', E_EMAIL.time) as day,
            COUNT(*) as events_email_count
        FROM events_email as E_EMAIL
        WHERE time >= :start_time
        GROUP BY day
    ) EVENTS_EMAIL
    ON EVENTS.day = EVENTS_EMAIL.day
    LEFT JOIN
    (
        SELECT
            date_trunc('day', E_PHONE.time) as day,
            COUNT(*) as events_phone_count
        FROM events_phone as E_PHONE
        WHERE time >= :start_time
        GROUP BY day
    ) EVENTS_PHONE
    ON EVENTS.day = EVENTS_PHONE.day
    LEFT JOIN
    (
        SELECT
            date_trunc('day', E_DEVICES.time) as day,
            COUNT(*) as events_devices_count
        FROM events_devices as E_DEVICES
        WHERE time >= :start_time
        GROUP BY day
    ) EVENTS_DEVICES
    ON EVENTS.day = EVENTS_DEVICES.day
    LEFT JOIN
    (
        SELECT
            date_trunc('day', PV.timestamp) as day,
            COUNT(*) as pageviews_count
        FROM pageviews as PV
        WHERE timestamp >= :start_time
        GROUP BY day
    ) PAGEVIEWS
    ON EVENTS.day = PAGEVIEWS.day
    ORDER BY EVENTS.day DESC;

Example Output (Updated on 2018-10-26)::

             day         | events_count | events_email_count | events_phone_count | events_devices_count | pageviews_count
    ---------------------+--------------+--------------------+--------------------+----------------------+-----------------
     2018-10-15 00:00:00 |      4440728 |              48945 |             277746 |              4440728 |         5387802
     2018-10-14 00:00:00 |      1924051 |              24420 |             115919 |              1924051 |         2397002
     2018-10-13 00:00:00 |      2025526 |              22063 |             124467 |              2025526 |         2508548
     2018-10-12 00:00:00 |      3826552 |              38251 |             240273 |              3826552 |         4572791
     2018-10-11 00:00:00 |      4288408 |              45851 |             278686 |              4287858 |         5404188


Does lambda have problems with invoke count, time duration, errors counts?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go AWS Console -> ``18-identity-analytics`` account -> lambda -> functions -> ``analytics-etl-prod`` (parser) ``analytics-etl-hot-prod`` (loader), take a look at Monitor Menu


Pin Point the Problem
------------------------------------------------------------------------------


Check Lambda Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. AWS Console -> ``18-identity-analytics`` account -> lambda -> functions -> ``analytics-etl-prod`` (parser) ``analytics-etl-hot-prod`` (loader)
2. Monitor Tab select missing data time range, check duration, and errors rate. avg duration for ``analytics-etl-prod`` is 10 ~ 12 seconds. avg for ``analytics-etl-hot-prod`` is around 5 minutes.
3. Select time range on dashboard, click the 3-dot button at top right on the plot -> View logs -> AWS/Lambda - /aws/lambda/<function-name>
4. Search ``REPORT``, it is the end of log in each invoke, you should search for ``TIMEOUT`` or ``OUT OF MEMORY`` problem.
5. Search ``ERROR``, find runtime exeception.


Check S3 Bucket
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. check ``s3://login-gov-prod-461353137281-us-west-2-analytics-hot/elk``, parsed files should be put here if ``analytics-etl-prod`` function works. If it is empty, it doesn't mean the ``analytics-etl-prod`` failed. Because ``analytics-etl-hot-prod`` will delete the file once parsed file is uploaded to Redshift. **If you can't observe any files in this bucket for long time, it means the parser failed**.

2. check ``s3://login-gov-prod-log/elk`` (in ``18-identity`` AWS account), randomly download some files, check if it has valid data.


Debug Parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Go Lambda Function ``analytics-etl-prod``, click Actions Menu, Export function, download source code.

execute the file you download with ``Uploader.etl`` method in ``src/uploader.py``.


Debug Loader
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute lambda handler ``function_2.lambda_handler`` locally.
