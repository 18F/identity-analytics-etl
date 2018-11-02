SELECT
    COUNT(DISTINCT events.user_id)
FROM events
WHERE
    events.name = 'User Registration: Email Confirmation'
    AND events.success IS TRUE;