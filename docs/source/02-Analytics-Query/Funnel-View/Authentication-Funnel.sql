/*
**Question**:

There are 9 primary phases in login.gov authentication flow.

1. Arrival from SP
2. Sign in page
3. Email attempt
4. Email attempt success
5. MFA Visited
6. MFA Attempt
7. Authentication complete (pre-handoff)
8. OIDC request
9. OIDC token

We want to know there are how many unique sessions in each phase.

**Definition**:

Arrival from SP:

Distinct count of unique visit_id with: "User Registration: intro visited" and exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

Sign in page:

Distinct count of unique visit_id with: "User Registration: intro visited" and ""Sign in page visited" and exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

Email attempt:

Distinct count of unique visit_id with: "User Registration: intro visited" and "Sign in page visited" and "Email and Password Authentication" and exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

Email attempt success:

Distinct count of unique visit_id with: "User Registration: intro visited" and "Sign in page visited" and ("Email and Password Authentication" where success=true) and exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

MFA Visited:

Distinct count of unique visit_id with: "User Registration: intro visited" and "Sign in page visited" and ("Email and Password Authentication" where success=true) and ("Multi-Factor Authentication: enter OTP visited' or "Multi-Factor Authentication: enter personal key visited") exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

MFA Attempt:

Distinct count of unique visit_id with: "User Registration: intro visited" and "Sign in page visited" and ("Email and Password Authentication" where success=true) and "Multi-Factor Authentication" exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

Authentication complete (pre-handoff):

Distinct count of unique visit_id with: "User Registration: intro visited" and "Sign in page visited" and ("Email and Password Authentication" where success=true) and ("Multi-Factor Authentication" where success=true) exclude events that have "User Registration: enter email visited" but not "Sign in page visited"

OIDC request:

definition are not finalized yet.

OIDC token:

definition are not finalized yet.

**SQL Description**:

**Database**: Redshift
*/

\set start_time '''2019-01-01'''
\set end_time '''2019-02-01'''

-- MAIN SUBQUERY, we only care about sessions from service provider
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

-- INTRO PAGE VISIT
t_ses_ids_that_intro_page_visit AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'User Registration: intro visited'
),

-- ENTER EMAIL
t_ses_ids_that_enter_email AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'User Registration: enter email visited'
),

-- SIGN IN PAGE VISIT
t_ses_ids_that_sign_in_page_visit AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'Sign in page visited'
),

-- ENTER EMAIL BUT NOT SIGN IN PAGE VISIT
t_ses_ids_that_enter_email_but_not_sign_in_page_visit AS (
    (SELECT * FROM t_ses_ids_that_enter_email)
    EXCEPT
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
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

-- MFA VISITED
t_ses_ids_mfa_visit AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication: enter OTP visited'
        OR E.name = 'Multi-Factor Authentication: enter personal key visited'
),

-- MFA ATTEMPT
t_ses_ids_mfa_attempt AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication'
),

-- MFA SUCCESS, AUTHENTICATION COMPLETE
t_ses_ids_mfa_attempt_success AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication'
        AND E.success IS TRUE
),

-- OIDC REQUEST
t_ses_ids_oidc_request AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'OpenID Connect: authorization request'
),

-- OIDC TOKEN
t_ses_ids_oidc_token AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'OpenID Connect: token'
),


-- Real count ---
t_arrival_from_sp AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    EXCEPT
    (SELECT * FROM t_ses_ids_that_enter_email_but_not_sign_in_page_visit)
),

t_sign_in_page_visit AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    EXCEPT
    (SELECT * FROM t_ses_ids_that_enter_email_but_not_sign_in_page_visit)
),

t_email_attempt AS (
    (SELECT * FROM t_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth)
),

t_email_attempt_success AS (
    (SELECT * FROM t_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
),

t_mfa_visit AS (
    (SELECT * FROM t_email_attempt_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_visit)
),

t_mfa_attempt AS (
    (SELECT * FROM t_mfa_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_attempt)
),

t_mfa_attempt_success AS (
    (SELECT * FROM t_mfa_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_attempt_success)
),

t_oidc_request AS (
    (SELECT * FROM t_mfa_attempt_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_oidc_request)
),

t_oidc_token AS (
    (SELECT * FROM t_mfa_attempt_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_oidc_token)
)

-- Organize Output
SELECT
    (SELECT COUNT(*) FROM t_arrival_from_sp) AS n_arrival_from_sp,
    (SELECT COUNT(*) FROM t_sign_in_page_visit) AS n_sign_in_page_visit,
    (SELECT COUNT(*) FROM t_email_attempt) AS n_email_attempt,
    (SELECT COUNT(*) FROM t_email_attempt_success) AS n_email_attempt_success,
    (SELECT COUNT(*) FROM t_mfa_visit) AS n_mfa_visit,
    (SELECT COUNT(*) FROM t_mfa_attempt) AS n_mfa_attempt,
    (SELECT COUNT(*) FROM t_mfa_attempt_success) AS n_authentiation_complete,
    (SELECT COUNT(*) FROM t_oidc_request) AS n_oidc_request,
    (SELECT COUNT(*) FROM t_oidc_token) AS n_oidc_token
;
