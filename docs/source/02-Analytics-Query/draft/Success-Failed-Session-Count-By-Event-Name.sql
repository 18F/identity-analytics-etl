/*
**Definition**:

How many success / failed **session** we have for each event name. **Only counts traffic from service providers**.

This helps us with success rate calculation.

You can pivot the result by ``success`` column in excel.

**Database**: Redshift
*/

\set start_time '''2019-01-01'''
\set end_time '''2019-01-02'''

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
ORDER BY name ASC, success DESC;
