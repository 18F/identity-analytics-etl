/*
**Definition**:

Number of users who use login.gov account to sign in to specific service provider first time by month.

**SQL Description**:

Similar to ``MFA-Completed-User-Count-by-SP.sql``.
*/

\set end_time '''2019-01-01'''

SELECT
    T_COUNT.identities_service_provider AS service_provider,
    service_providers.friendly_name AS friendly_name,
    service_providers.return_to_sp_url AS return_to_sp_url,
    T_COUNT.month AS month,
    T_COUNT.user_count AS user_count
FROM
(
    SELECT
        T_ID.service_provider AS identities_service_provider,
        date_trunc('month', T_ID.created_at) AS month,
        COUNT(T_ID.user_id) AS user_count
    FROM (
        SELECT *
        FROM identities
        WHERE identities.created_at < :end_time
    ) T_ID
    GROUP BY identities_service_provider, month
    ORDER BY identities_service_provider DESC, month DESC
) T_COUNT
JOIN service_providers
ON T_COUNT.identities_service_provider = service_providers.issuer;