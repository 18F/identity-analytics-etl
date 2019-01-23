/*
**Definition**:

How many new users finished login.gov signup (MFA completed) every month.

**SQL Description**:

User may have multiple MFA method setup, use the earliest one as MFA signup time.
*/

SELECT
    T.signup_month AS signup_month,
    COUNT(*) AS mfa_user_count
FROM
(
    -- join three table, use the earliest sign up time
    SELECT
        T_PHONE.user_id AS user_id,
        date_trunc('month', LEAST(T_PHONE.signup_time, T_ID.signup_time, T_WEBAUTH.signup_time)) AS signup_month
    FROM (
        SELECT
            phone_configurations.user_id AS user_id,
            MIN(phone_configurations.confirmed_at) AS signup_time
        FROM phone_configurations
        GROUP BY phone_configurations.user_id
    ) T_PHONE
    FULL OUTER JOIN
    (
        SELECT
            identities.user_id AS user_id,
            MIN(identities.created_at) AS signup_time
        FROM identities
        GROUP BY identities.user_id
    ) T_ID
        ON T_PHONE.user_id = T_ID.user_id
    FULL OUTER JOIN
    (
        SELECT
            webauthn_configurations.user_id AS user_id,
            MIN(webauthn_configurations.created_at) AS signup_time
        FROM webauthn_configurations
        GROUP BY webauthn_configurations.user_id
    ) T_WEBAUTH
        ON T_ID.user_id = T_WEBAUTH.user_id
) T
GROUP BY signup_month
ORDER BY signup_month DESC;
