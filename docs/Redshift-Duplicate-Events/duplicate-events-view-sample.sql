/*
This query returns list of event_id with duplicate data.

Then you can use this query to explore some samples:

.. code-block:: SQL

    SELECT *
    FROM events
    WHERE events.id = 'the_event_id_string';
*/

SELECT
    T_ID_COUNT.id,
    T_ID_COUNT.id_count
FROM (
    SELECT
        events.id as id,
        COUNT(events.id) as id_count
    FROM events
    GROUP BY events.id
) T_ID_COUNT
WHERE T_ID_COUNT.id_count >= 2
ORDER BY T_ID_COUNT.id_count DESC
LIMIT 1000;
