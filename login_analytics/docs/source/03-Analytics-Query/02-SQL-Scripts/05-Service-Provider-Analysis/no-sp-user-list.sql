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
;