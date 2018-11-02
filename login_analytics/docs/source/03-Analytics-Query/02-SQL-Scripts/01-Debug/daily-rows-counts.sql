/*
This SQL exams number of rows by date from certain time.

This scripts is for checking if our ETL pipeline broken.
*/

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