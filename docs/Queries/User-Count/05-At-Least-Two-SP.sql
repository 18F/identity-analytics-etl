/*
**Definition**: number of Users who created their Login.gov account and completed registering MFA as a result of initiating their Login.gov session through at least TWO SP.

**SQL Description**:

unlike ``users`` table, any users in ``identities`` have been finished MFA setup.

**Database**: IDP-DB
*/

\set end_time '''2019-01-01'''
SELECT COUNT(T.user_id) AS at_least_2sp_user_counts
FROM (
    SELECT
        identities.user_id as user_id
    FROM identities
    WHERE identities.created_at < :end_time
    GROUP BY user_id
    HAVING COUNT(identities.user_id) >= 2
) AS T;
