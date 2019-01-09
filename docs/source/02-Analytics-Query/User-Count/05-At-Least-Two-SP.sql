/*
**Definition**: number of Users who created their Login.gov account and completed registering MFA as a result of initiating their Login.gov session through that SP.

**SQL Description**:

unlike ``users`` table, any users in ``identities`` have been finished MFA setup.
*/

\set end_time '''2019-01-01'''
SELECT
    (COUNT(identities.user_id) - COUNT(DISTINCT(identities.user_id))) AS at_least_2sp_user_counts
FROM identities
WHERE identities.created_at < :end_time;