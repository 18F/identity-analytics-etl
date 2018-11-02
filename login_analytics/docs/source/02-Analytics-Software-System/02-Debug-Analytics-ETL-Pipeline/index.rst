.. contents::

.. _debug_analytics_etl_pipeline:

Debug Analytics ETL Pipeline
==============================================================================

The ETL pipeline copies parsed data into these tables:

- :ref:`prod.redshift.schema.table.events`:
- :ref:`prod.redshift.schema.table.events_devices`:
- :ref:`prod.redshift.schema.table.events_email`:
- :ref:`prod.redshift.schema.table.events_phone`:
- :ref:`prod.redshift.schema.table.pageviews`:

For Redshift Schema, click :ref:`prod.redshift.schema.database`.

This is the Analytic ETL pipeline **Data Flow Diagram**. Failure of any component or operation could be the reason.

.. raw:: html

    <!--[if IE]><meta http-equiv="X-UA-Compatible" content="IE=5,IE=9" ><![endif]-->
    <!DOCTYPE html>
    <html>
    <head>
    <title>Analytics-ETL-Pipeline</title>
    <meta charset="utf-8"/>
    </head>
    <body><div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile userAgent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36\&quot; version=\&quot;9.3.0\&quot; editor=\&quot;www.draw.io\&quot; type=\&quot;device\&quot;&gt;&lt;diagram id=\&quot;a6f997ca-872b-3d3f-56a5-e97fb92471e1\&quot; name=\&quot;Page-1\&quot;&gt;zVjbbuIwEP2avCI7hsI+buntoStVZaVtH10yJN46ceQ4hezXr42dG25R1TYpPEB8fBufOTNjEpBluruWNE9+iQh4EKJoF5CLIAznZKG/DVBZYIqJBWLJIgvhFlixf+BA5NCSRVD0BiohuGJ5H1yLLIO16mFUSrHtD9sI3t81pzF4wGpNuY/+YZFKLLqYoRa/ARYn9c4YuZ4nun6OpSgzt18Qks3+Y7tTWq/lxhcJjcS2A5HLgCylEMo+pbslcENtTZudd/VGb2O3hEy9Z8LUTnihvKyPPtHtFegDhOiCKursVFXNDUSaKtcUUiUiFhnlly16vj8/mB2QbiUq5foR60fYMfVg4MnMtR7rnkzJqtNlmo9ugb+gVOU0QkslNNTueytE7tawlhrz3iTDQYUo5dqNCp28qIzBjSKNI7S+QaSgjdFDJHCq2Et/deqUFjfjWrb1gyP8dfJDj/xbEccsi40HqkJB6pHfp3abMAWrnO7PstWR2KfbLQ9Swe44Jf5h3YSF02nVb27boMC1lJNOQEzR59mpc0GHHmK0eUdlAcOocn5ElvORdUl8Xc5G0iXxiF9Zw7QsdR86L9fP2qYT02aIRhTnD4+i0GjzHmg0jDTDrjRRX5phT5p4cGnOvi9lYj9nTjsF6x6KkvvK/AIP4C79bY166Hqj7Rudf/xGqHy5A2Z+zaLpU0St1QXIU0sLJByzZmGPnht9lTutvNkw8i0M+TfOmQnga0MM2jBuqgxnxSBBfJBG8bE0OnyFx6+U+NHiGPuBfGb88FuyODZRjJYir/Y/aUqzgara/LCqjcH4J9h1U+8Ey1QbUFPcD6gmeOolrIfdrAMfNWa8z23+3azJv1zQ6ATy72F6GfVehuceP/NJK+ah/tAeuR3gYOTbAT4bIK3sp/6UkladAbkRdHEkLg5Kcf2W5Oqd48kUHfjeWvDh4DnzxHEPUZGwzekV5QH/aetm+4LJ0ti+xCOX/wE=&lt;/diagram&gt;&lt;/mxfile&gt;&quot;}"></div>
    <script type="text/javascript" src="https://www.draw.io/js/viewer.min.js"></script>
    </body>
    </html>

Login to ``18f-identity-analytics`` AWS Account account: https://18f-identity-analytics.signin.aws.amazon.com/console

:ref:`prod.redshift.schema.database`

The ETL pipeline copies parsed data into these tables:

- :ref:`prod.redshift.schema.table.events`:
- :ref:`prod.redshift.schema.table.events_devices`:
- :ref:`prod.redshift.schema.table.events_email`:
- :ref:`prod.redshift.schema.table.events_phone`:
- :ref:`prod.redshift.schema.table.pageviews`:


1. Do we have data in Redshift?
------------------------------------------------------------------------------

This sql scripts gives you counts of rows we copied every days. You can visually check if there is missing data.

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


2. Does lambda function actively working?
------------------------------------------------------------------------------

1. Open ``18f-analytics`` AWS console, go to ``lambda function``.
2. Open `analytics-etl-prod <https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/analytics-etl-prod?tab=monitoring>`_ (Lambda parser), and `analytics-etl-prod-hot <https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2#/functions/analytics-etl-prod-hot?tab=graph>`_ (Lambda loader), check 3h, 3d, 1w ``Invocations``, ``Duration``, ``Erros, Availability`` monitor.


3. Is the source data valid?
------------------------------------------------------------------------------

You have to check the log files in `18f-identity/login-gov-prod-logs` bucket.

To get help for setup your AWS account, click :ref:`aws-account`.