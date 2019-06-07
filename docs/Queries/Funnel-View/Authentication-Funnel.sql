/*
Authentication drop off rate by step

Steps in authenication
1. Sign up page
2. Enter email
3. Enter email successfully
4. Visit MFA page (or bypass because remembered device)
5. Enter MFA
6. Complete Auth
*/


\set starttime '''2019-05-10'''
\set endtime '''2019-06-01'''

-- MAIN SUBQUERY, we only care about sessions from service provider
WITH E AS (
    SELECT
        events.name AS name,
        events.visit_id AS ses_id,
        events.event_properties AS event_properties,
        events.success AS success
    FROM events
    WHERE
        events.time BETWEEN :starttime AND :endtime
        AND events.service_provider IS NOT NULL
        AND events.service_provider != ''
),

-- SIGN IN PAGE VISIT
t_ses_ids_that_sign_in_page_visit AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'Sign in page visited'
),

-- EMAIL AND PASSWORD AUTH
t_ses_ids_that_email_pass_auth AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'Email and Password Authentication'
),

-- SUCCESS EMAIL AND PASSWORD AUTH
t_ses_ids_that_email_pass_auth_success AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Email and Password Authentication'
        AND E.success IS TRUE
),

-- SUCCESS EMAIL AND PASSWORD AUTH WITH DEVICE REMEMBERED
t_ses_ids_with_device_remembered AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User marked authenticated'
        AND json_extract_path_text(E.event_properties, 'authentication_type') = 'device_remembered'
),

-- MFA VISITED
t_ses_ids_mfa_visit AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name LIKE 'Multi-Factor Authentication: enter %'

),

t_ses_ids_mfa_visit_with_device_remembered AS (
    (SELECT * FROM t_ses_ids_mfa_visit)
    UNION
    (SELECT * FROM t_ses_ids_with_device_remembered)
),

-- MFA ATTEMPT
t_ses_ids_mfa_attempt AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication'
),

t_ses_ids_mfa_attempt_with_device_remembered AS (
    (SELECT * FROM t_ses_ids_mfa_attempt)
    UNION
    (SELECT * FROM t_ses_ids_with_device_remembered)
),

-- MFA SUCCESS, AUTHENTICATION COMPLETE
t_ses_ids_mfa_complete AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'User marked authenticated'
),

-- OIDC REQUEST
t_ses_ids_oidc_request AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'OpenID Connect: authorization request'
),

-- OIDC REQUEST SUCCESS
t_ses_ids_oidc_request_success AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'OpenID Connect: authorization request'
        AND E.success IS TRUE
),

-- Aggregations
t_sign_in_page_visit AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
),
t_enter_email AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth)
),
t_enter_email_success AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
),
t_mfa_visits AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_visit_with_device_remembered)
),
t_mfa_attempt AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_attempt_with_device_remembered)
),

t_mfa_complete AS (
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_complete)

),

t_oidc_request AS (
    (SELECT * FROM t_ses_ids_mfa_complete)
    INTERSECT
    (SELECT * FROM t_ses_ids_oidc_request_success)
)

-- Organize Output
SELECT
    (SELECT COUNT(*) FROM t_sign_in_page_visit) AS sign_in_page_visit,
    (SELECT COUNT(*) FROM t_enter_email) AS enter_email,
    (SELECT COUNT(*) FROM t_enter_email_success) AS email_attempt_success,
    (SELECT COUNT(*) FROM t_mfa_visits) AS mfa_visits,
    (SELECT COUNT(*) FROM t_mfa_attempt) AS mfa_attempts,
    (SELECT COUNT(*) FROM t_mfa_complete) AS n_authentiation_complete,
    (SELECT COUNT(*) FROM t_oidc_request) AS n_oidc_request
;

