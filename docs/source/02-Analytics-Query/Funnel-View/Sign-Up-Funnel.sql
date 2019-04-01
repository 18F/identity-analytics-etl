/*
**Question**:

There are 8 primary phases in login.gov sign-up flow that the user is from a service provider.

1. User has entered a valid email
2. User has entered a confirmation email
3. User has created a valid password
4. User has visited the MFA setup page
5. User has finished MFA setup
6. User has viewed personal key page
7. User has visited hand-off page with service provider
8. Sign-up workflow is finished, user is on service provider website

We want to know how many unique sessions are there in each phase.

**Definition**:

1. User has entered a valid email::

    if have 'User Registration: Email Submitted' and success = True
        return True

2. User has entered a confirmation email::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        return True

3. User has created a valid password::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        return True

4. User has visited the MFA setup page::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        AND (have 'User Registration: 2FA Setup visited')
        return True

5. User has finished MFA setup::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        AND (have 'User Registration: 2FA Setup visited')
        AND (have 'User Registration: 2FA Setup' and success = True)
        AND (
            (have 'Multi-Factor Authentication: phone setup' and success = True)
            OR
            (have 'Multi-Factor Authentication Setup' and success = True)
            (have 'WebAuthn Setup Visited' and success = True)
            (have 'Multi-Factor Authentication: enter backup code visited')
        )
        return True

6. User has viewed personal key page::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        AND (have 'User Registration: 2FA Setup visited')
        AND (have 'User Registration: 2FA Setup' and success = True)
        AND (
            (have 'Multi-Factor Authentication: phone setup' and success = True)
            OR
            (have 'Multi-Factor Authentication Setup' and success = True)
            (have 'WebAuthn Setup Visited' and success = True)
            (have 'Multi-Factor Authentication: enter backup code visited')
        )
        AND (have 'User Registration: personal key visited')
        return True


7. User has visited hand-off page with service provider::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        AND (have 'User Registration: 2FA Setup visited')
        AND (have 'User Registration: 2FA Setup' and success = True)
        AND (
            (have 'Multi-Factor Authentication: phone setup' and success = True)
            OR
            (have 'Multi-Factor Authentication Setup' and success = True)
            (have 'WebAuthn Setup Visited' and success = True)
            (have 'Multi-Factor Authentication: enter backup code visited')
        )
        AND (have 'User Registration: personal key visited')
        AND (have 'User registration: agency handoff visited')
        return True

8. Sign-up workflow is finished, user is on service provider website::

    if (have 'User Registration: Email Submitted' and success = True)
        AND (have 'User Registration: Email Confirmation' and success = True)
        AND (have 'Password Creation' and success = True)
        AND (have 'User Registration: 2FA Setup visited')
        AND (have 'User Registration: 2FA Setup' and success = True)
        AND (
            (have 'Multi-Factor Authentication: phone setup' and success = True)
            OR
            (have 'Multi-Factor Authentication Setup' and success = True)
            (have 'WebAuthn Setup Visited' and success = True)
            (have 'Multi-Factor Authentication: enter backup code visited')
        )
        AND (have 'User Registration: personal key visited')
        AND (have 'User registration: agency handoff visited')
        AND (have 'User registration: agency handoff complete')
        return True
*/

\set starttime '''2019-01-01'''
\set endtime '''2019-02-01'''

WITH E AS (
    SELECT
        events.name AS name,
        events.visit_id AS ses_id,
        events.success AS success
    FROM events
    WHERE
        events.time BETWEEN :starttime AND :endtime
        AND events.service_provider IS NOT NULL
        AND events.service_provider != ''
),


t_ses_id_email_entered AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User Registration: Email Submitted'
        AND E.success IS TRUE
),


t_ses_id_email_confirmation AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User Registration: Email Confirmation'
        AND E.success IS TRUE
),


t_ses_id_password_creation AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Password Creation'
        AND E.success IS TRUE
),


t_ses_id_mfa_setup_visited AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User Registration: 2FA Setup visited'
),


-- MFA Methods
t_ses_id_2fa_setup AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User Registration: 2FA Setup'
        AND E.success IS TRUE
),


-- text message or phone call
t_ses_id_mfa_phone_setup AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication: phone setup'
        AND E.success IS TRUE
),


-- authentication app
t_ses_id_mfa_setup AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication Setup'
        AND E.success IS TRUE
),


-- web auth
t_ses_id_mfa_web_app_setup AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'WebAuthn Setup Visited'
        AND E.success IS TRUE
),


-- backup code
t_ses_id_mfa_backup_code_setup AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication: enter backup code visited'
),


t_ses_id_at_least_one_mfa_method_setup_success AS (
    (SELECT * FROM t_ses_id_mfa_phone_setup)
    UNION
    (SELECT * FROM t_ses_id_mfa_setup)
    UNION
    (SELECT * FROM t_ses_id_mfa_web_app_setup)
    UNION
    (SELECT * FROM t_ses_id_mfa_backup_code_setup)
),


t_ses_id_mfa_setup_complete AS (
    (SELECT * FROM t_ses_id_2fa_setup)
    INTERSECT
    (SELECT * FROM t_ses_id_at_least_one_mfa_method_setup_success)
),


-- after MFA setup
t_ses_id_personal_key_visited AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User Registration: personal key visited'
),


t_ses_id_agency_handoff_visited AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User registration: agency handoff visited'
),

t_ses_id_agency_handoff_complete AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User registration: agency handoff complete'
),

-- **Real count** ---
t_step1_email_entered AS (
    (SELECT * FROM t_ses_id_email_entered)
),


t_step2_email_confirmed AS (
    (SELECT * FROM t_step1_email_entered)
    INTERSECT
    (SELECT * FROM t_ses_id_email_confirmation)
),


t_step3_password_created AS (
    (SELECT * FROM t_step2_email_confirmed)
    INTERSECT
    (SELECT * FROM t_ses_id_password_creation)
),


t_step4_mfa_setup_visited AS (
    (SELECT * FROM t_step3_password_created)
    INTERSECT
    (SELECT * FROM t_ses_id_mfa_setup_visited)
),


t_step5_mfa_setup_complete AS (
    (SELECT * FROM t_step4_mfa_setup_visited)
    INTERSECT
    (SELECT * FROM t_ses_id_mfa_setup_complete)
),


t_step6_view_personal_key AS (
    (SELECT * FROM t_step5_mfa_setup_complete)
    INTERSECT
    (SELECT * FROM t_ses_id_personal_key_visited)
),


t_step7_hand_off AS (
    (SELECT * FROM t_step6_view_personal_key)
    INTERSECT
    (SELECT * FROM t_ses_id_agency_handoff_visited)
),


t_step8_registration_complete AS (
    (SELECT * FROM t_step7_hand_off)
    INTERSECT
    (SELECT * FROM t_ses_id_agency_handoff_complete)
)

-- Organize Output
SELECT
    (SELECT COUNT(*) FROM t_step1_email_entered) AS n_email_entered,
    (SELECT COUNT(*) FROM t_step2_email_confirmed) AS n_email_confirmed,
    (SELECT COUNT(*) FROM t_step3_password_created) AS n_pwd_created,
    (SELECT COUNT(*) FROM t_step4_mfa_setup_visited) AS n_mfa_setup_visit,
    (SELECT COUNT(*) FROM t_step5_mfa_setup_complete) AS n_mfa_setup_done,
    (SELECT COUNT(*) FROM t_step6_view_personal_key) AS n_view_personal_key,
    (SELECT COUNT(*) FROM t_step7_hand_off) AS n_hand_off,
    (SELECT COUNT(*) FROM t_step8_registration_complete) AS n_signup_done
;