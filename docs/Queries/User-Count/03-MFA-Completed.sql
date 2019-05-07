/*
**Definition**: Counting users as a whole - MFA Completed

We have these MFA options:

1. Personal Key.
2. Phone or Text. (majority, 80% +)
3. Web Auth, a FIDO hardware security keys.
4. Auth App.

If a user has any of these method setup, we count him as a **MFA Complete**.

The MFA Setup workflow is: ``Email Password Signup`` -> ``The default Personal Key MFA Setup`` -> ``Additional MFA Method Setup``.

**SQL Explanation**:

1. ``users.confirmed_at`` is created when user finished email password signup.
2. Then user goes to MFA signup, personal key is the default and "always-have" MFA method. Once it is done, ``users.encrypted_recovery_code_digest`` been created. **BUT, there’s no timestamp info for this event**.
3. Then user is able to create additional MFA method, for example, Phone/Text. Then ``phone_configurations.phone_confirmed_at`` will be created.
4. If user successfully sign in to any service provider with any MFA method, a data entry will be created in ``table.identites``.

Since there's no explicit time info for the moment user finished the default MFA Method Setup, it is impossible to get the accurate count. However, we can still estimate the number. The total actual count has to be less than using ``users.confirmed_at``, and greater than using ``users.phone_confirmed_at``, and also greater than using ``identities.created_at``.

MFA count on ``2018-12-31 23:59:59`` is 11055433;

**Database**: IDP-DB
*/

\set end_time '''2019-01-01'''
SELECT COUNT(*) as mfa_complete_count
FROM (
    (
        SELECT DISTINCT(phone_configurations.user_id) AS user_id
        FROM phone_configurations
        WHERE phone_configurations.confirmed_at < :end_time
    ) UNION
    (
        SELECT DISTINCT(identities.user_id) AS user_id
        FROM identities
        WHERE identities.created_at < :end_time
    ) UNION
    (
        SELECT DISTINCT(webauthn_configurations.user_id) AS user_id
        FROM webauthn_configurations
        WHERE webauthn_configurations.created_at < :end_time
    )
) AS T;
