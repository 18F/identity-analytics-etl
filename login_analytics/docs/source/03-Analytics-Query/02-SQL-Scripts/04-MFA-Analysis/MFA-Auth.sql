/*
This query selects successful MFA auth events.
*/

SELECT *
FROM events
WHERE
    events.name = 'Multi-Factor Authentication'
    AND events.context = 'authentication'
    AND events.success IS TRUE
LIMIT 10;


SELECT *
FROM events
WHERE
    events.name = 'Multi-Factor Authentication'
    AND events.context = 'authentication'
    AND events.success IS TRUE
    AND events.user_id = '67c55c91-a819-4367-bd38-4505d72fb7ce'
    AND events.service_provider IS NOT NULL
ORDER BY events.time ASC
LIMIT 1;