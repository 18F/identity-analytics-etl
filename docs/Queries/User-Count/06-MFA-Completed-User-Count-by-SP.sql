/*
**Definition**:

Number of Users who created their Login.gov account and completed registering MFA as a result of initiating their Login.gov session through that SP.

**SQL Description**:

unlike ``users`` table, any users in ``identities`` have been finished MFA setup.

.. code-block:: SQL

    SELECT COUNT(DISTINCT(identities.user_id)) FROM identities;

Verify ``identities.service_provider`` is not nullable:

.. code-block:: SQL

    -- result = 0
    SELECT COUNT(*)
    FROM identities
    WHERE identities.service_provider IS NULL;

Verify ``identities.user_id`` is not nullable:

.. code-block:: SQL

    -- result = 0
    SELECT COUNT(*)
    FROM identities
    WHERE identities.user_id IS NULL;

**Database**: IDP-DB
*/

\set end_time '''2019-01-01'''
SELECT
    E.identities_service_provider as service_provider,
    service_providers.friendly_name as friendly_name,
    service_providers.return_to_sp_url as return_to_sp_url,
    E.count_user_id as user_count
FROM
(
    SELECT
        COUNT(identities.user_id) AS count_user_id,
        identities.service_provider AS identities_service_provider
    FROM identities
    WHERE
        identities.created_at < :end_time;
    GROUP BY identities.service_provider
) as E
FULL OUTER JOIN service_providers
ON E.identities_service_provider = service_providers.issuer
ORDER BY user_count DESC;
