/*
**Definition**:

We want to compare data quality in redshift to its source cloudwatch log.

How many events we have for different event name can gives us clear information about how many events are missing compared to cloudwatch.

**It helps us making decision on whether we should use Redshift for specific question**

**SQL Description**:

Defines the criterion, data points. parameters (e.g. ``start_time`` and ``end_time``).

**Database**: Redshift
*/

\set start_time '''2019-01-01'''
\set end_time '''2019-01-02'''

SELECT
    T1.name as name1,
    T2.name as name2,
    T1.n_event as n_event,
    T2.n_success_event as n_success_event,
    T2.n_success_event * 1.0 / T1.n_event as success_rate
FROM (
    SELECT
        events.name as name,
        COUNT(events.name) as n_event
    FROM events
    WHERE
        events.time BETWEEN :start_time AND :end_time
    GROUP BY events.name
) T1
JOIN
(
    SELECT
        events.name as name,
        COUNT(events.name) as n_success_event
    FROM events
    WHERE
        events.time BETWEEN :start_time AND :end_time
        AND events.success IS TRUE
    GROUP BY events.name
) T2
ON T1.name = T2.name
ORDER BY name1;
