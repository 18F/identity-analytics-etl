/*
This query displays the total number and percentage of duplicate events in redshift.

- total_events: total number of rows in event table
- unique_events: number of distinct event
- duplicate_events: number of duplicate data
- duplicate_perc: percentage of duplicate data
*/

SELECT
    (
        SELECT COUNT(events.id) FROM events
    ) AS total_events,
    (
        SELECT COUNT(DISTINCT(events.id)) FROM events
    ) AS unique_events,
    (total_events - unique_events) AS duplicate_events,
    (duplicate_events * 1.0 / total_events) AS duplicate_perc; -- 0.7 % on 2019-01-01
