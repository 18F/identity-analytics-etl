/*
**Definition**: Counting users as a whole - Email Confirmed

**SQL Description**:

Users will receive an confirmation email with a link. And the time they clicked
the link will be stored in ``users.confirmed_at`` field.

Remove the ``\set end_time ...`` and ``WHERE ... < :end_time`` line For most recent result.
*/

\set end_time '''2019-01-01'''
SELECT COUNT(users.confirmed_at)
FROM users
WHERE
    users.confirmed_at IS NOT NULL
    AND users.confirmed_at < :end_time;
