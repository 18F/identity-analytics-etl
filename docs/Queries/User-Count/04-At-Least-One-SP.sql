/*
**Definition**: number of Users who created their Login.gov account and completed registering MFA as a result of initiating their Login.gov session through at least one SP.

**SQL Description**:

unlike ``users`` table, any users in ``identities`` have been finished MFA setup.

**Database**: IDP-DB
*/

\set end_time '''2019-01-01'''
SELECT
    COUNT(DISTINCT(identities.user_id)) AS at_least_1sp_user_counts
FROM identities
WHERE identities.created_at < :end_time;