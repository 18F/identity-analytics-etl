SELECT
    COUNT(DISTINCT user_id) AS counts
FROM
(
    SELECT
        events.user_id
    FROM events
    GROUP BY events.user_id
    HAVING
        max(CASE WHEN events.name = 'Email and Password Authentication' AND events.success IS TRUE THEN 1 ELSE 0 END) = 0
) E;