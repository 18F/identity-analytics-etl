/*
**Definition**:

How many success / failed **session** we have for each event name. **Only counts traffic from service providers**.

This helps us with success rate calculation.

**Database**: Redshift
*/

\set start_time '''2019-02-21'''
\set end_time '''2019-02-22'''

SELECT
    T.name as name,
    SUM(case when T.success IS TRUE then T.n_sessions else 0 end) AS n_success,
    SUM(case when T.success IS FALSE then T.n_sessions else 0 end) AS n_failed,
    SUM(case when T.success IS NULL then T.n_sessions else 0 end) AS n_null,
    SUM(T.n_sessions) AS n_total
FROM (
    SELECT
        events.name as name,
        events.success as success,
        COUNT(DISTINCT(events.visit_id)) as n_sessions
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
