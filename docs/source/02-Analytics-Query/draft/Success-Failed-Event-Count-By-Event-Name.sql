/*
**Definition**:

We want to compare data quality in redshift to its source Cloudwatch log.

How many events we have for each event name can tell how many events are missing in Redshift.

Since we use event name heavily, **it helps us making decision on whether we should use Redshift for specific question**.

You can pivot the result by ``success`` column in excel.

**Database**: Redshift
*/

\set start_time '''2019-01-01'''
\set end_time '''2019-01-02'''

SELECT
    events.name as name,
    events.success as success,
    COUNT(*) as n_events
FROM events
WHERE
    events.time BETWEEN :start_time AND :end_time
GROUP BY name, success
ORDER BY name ASC, success DESC;
