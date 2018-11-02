/*
This SQL returns number of unique users that entered their email address.
Maybe confirmed, maybe not.
*/
SELECT
    COUNT(DISTINCT events.user_id)
FROM events
WHERE
    events.name = 'User Registration: Email Submitted'
    AND events.success IS TRUE;