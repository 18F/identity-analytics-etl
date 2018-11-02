/*
Count of users that:

1. has at least one successful sign in.
2. only has events with empty sp

Result (2018-10-30): 600075
*/

SELECT
    COUNT(T1.user_id)
FROM
(
    -- user_id list that only has empty service provider
    SELECT
        T_USR_MAIN_SP.user_id as user_id
    FROM
    (
        SELECT
            events.user_id as user_id,
            MIN(events.service_provider) as sp
        FROM events
        GROUP BY events.user_id
        HAVING
            COUNT(DISTINCT events.service_provider) = 1
    ) T_USR_MAIN_SP
    WHERE T_USR_MAIN_SP.sp = ''
) T1
-- intersection of
INNER JOIN
(
    -- user_id list that has at least one successful sign in.
    SELECT
        events.user_id as user_id
    FROM events
    WHERE
        events.name = 'Email and Password Authentication'
        AND events.success IS TRUE
    GROUP BY events.user_id
) T2
ON T1.user_id = T2.user_id;