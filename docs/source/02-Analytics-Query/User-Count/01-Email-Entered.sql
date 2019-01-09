/*
**Definition**: Counting users as a whole - Email Entered

**SQL Explanation**:

An user record will be created in ``users`` table when they entered their email.
And the time they created will be stored in ``users.created_at`` field

**Note**:

Remove the ``\set end_time ...`` and ``WHERE ... < :end_time`` line For most recent result.
*/

\set end_time '''2019-01-01'''
SELECT COUNT(users.id)
FROM users
WHERE users.created_at < :end_time;
