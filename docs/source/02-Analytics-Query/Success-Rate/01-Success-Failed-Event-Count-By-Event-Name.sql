/*
**Definition**:

We want to compare data quality in redshift to its source Cloudwatch log.

How many events we have for each event name can tell how many events are missing in Redshift. **Only counts traffic from service providers**.

Since we use event name heavily, **it helps us making decision on whether we should use Redshift for specific question**.

**Database**: Redshift
*/

\set start_time '''2019-02-21'''
\set end_time '''2019-02-22'''

SELECT
    T.name as name,
    SUM(case when T.success IS TRUE then T.n_events else 0 end) AS n_success,
    SUM(case when T.success IS FALSE then T.n_events else 0 end) AS n_failed,
    SUM(case when T.success IS NULL then T.n_events else 0 end) AS n_null,
    SUM(T.n_events) AS n_total
FROM (
    SELECT
        events.name as name,
        events.success as success,
        COUNT(*) as n_events
    FROM events
    WHERE
        events.time BETWEEN :start_time AND :end_time
        AND events.service_provider IS NOT NULL
        AND events.service_provider != ''
    GROUP BY name, success
    ORDER BY name ASC, success DESC
) T
GROUP BY name
ORDER BY name;
