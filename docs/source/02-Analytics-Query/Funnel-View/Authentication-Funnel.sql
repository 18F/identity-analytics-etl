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

We want to know how many unique sessions are there in each phase.

**Definition**:

Arrival from SP:

if "User Registration: intro visited":
    if NOT "User Registration: enter email visited":
        return true
    else:
        if ("Sign in page visited"):
            return true
        else:
            return false

Sign in page:

if "User Registration: intro visited":
    and ("Sign in page visited):
        return true

Email attempt:

if "User Registration: intro visited"
    and "Sign in page visited"
    and "Email and Password Authentication":
        return true

Email attempt success:

if "User Registration: intro visited"
    and "Sign in page visited"
    and ("Email and Password Authentication" and properties.success=true):
        return true

MFA Visited:

if "User Registration: intro visited"
    and "Sign in page visited
    and ("Email and Password Authentication" and properties.success=true)
    and [
        (
            "Multi-Factor Authentication: enter OTP visited"
            or "Multi-Factor Authentication: enter personal key visited"
        )
        or (
            "Email and Password Authentication"
            and properties.success=true
            and properties.remember_device=true
        )
    ]
    return true

MFA Attempt:

if "User Registration: intro visited"
    and "Sign in page visited"
    and ("Email and Password Authentication" and properties.success=true)
    and [
        [
            (
                "Multi-Factor Authentication: enter OTP visited"
                or "Multi-Factor Authentication: enter personal key visited"
            )
            and ("Multi-Factor Authentication")
        ]
        or (
            "Email and Password Authentication"
            and properties.success=true
            and properties.remember_device=true
        )
    ]
    return true

Authentication complete (pre-handoff):

if "User Registration: intro visited"
    and "Sign in page visited"
    and ("Email and Password Authentication" and properties.success=true)
    and [
        [
            (
                "Multi-Factor Authentication: enter OTP visited"
                or "Multi-Factor Authentication: enter personal key visited"
            )
            and ("Multi-Factor Authentication" and properties.success=true)
        ]
        or (
            "Email and Password Authentication"
            and properties.success=true
            and properties.remember_device=true
        )
    ]
    return true

OIDC request:

if [("User Registration: intro visited")
    and ("Sign in page visited)
    and ("Email and Password Authentication" and properties.success=true)
    and [
        [
            (
                "Multi-Factor Authentication: enter OTP visited"
                or "Multi-Factor Authentication: enter personal key visited"
            )
            and (
                "Multi-Factor Authentication"
                and properties.success=true
            )
            and "OpenID Connect: authorization request"
        ]
        or
        (
            "Email and Password Authentication"
            and properties.success=true
            and properties.remember_device=true
        )
    ]
    return true

**SQL Description**:

Use ``GROUP BY visit_id HAVING ...`` is not efficient and hard to extend by adding more criterion. A better solution is to find the distinct visit_id based on different criterion, and use set operation such as UNION, INTERSECT, EXCEPT to answer the question, which is faster and easier to understand.

**Database**: Redshift
*/

\set starttime '''2019-01-01'''
\set endtime '''2019-02-01'''

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

-- SUCCESS EMAIL AND PASSWORD AUTH WITH DEVICE REMEMBERED
t_ses_ids_that_email_pass_auth_success_with_device_remembered AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Email and Password Authentication'
        AND E.success IS TRUE
        AND json_extract_path_text(E.event_properties, 'remember_device') = 'true'
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

-- MFA VISITED WITH DEVICE REMEMBERED
t_ses_ids_mfa_visit_with_device_remembered AS (
    (SELECT * FROM t_ses_ids_mfa_visit)
    UNION
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success_with_device_remembered)
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

-- OIDC REQUEST SUCCESS
t_ses_ids_oidc_request_success AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'OpenID Connect: authorization request'
        AND E.success IS TRUE
),

-- **Real count** ---
t_arrival_from_sp AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    EXCEPT
    (SELECT * FROM t_ses_ids_that_enter_email_but_not_sign_in_page_visit)
),

t_sign_in_page_visit AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
),

t_email_attempt AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth)
),

t_email_attempt_success AS (
    (SELECT * FROM t_ses_ids_that_intro_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_sign_in_page_visit)
    INTERSECT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
),

t_mfa_visit AS (
    (SELECT * FROM t_email_attempt_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_mfa_visit_with_device_remembered)
),

t_mfa_attempt AS (
    (SELECT * FROM t_email_attempt_success)
    INTERSECT
    (
        SELECT * FROM (
            (
                SELECT * FROM (
                    (SELECT * FROM t_ses_ids_mfa_visit)
                    INTERSECT
                    (SELECT * FROM t_ses_ids_mfa_attempt)
                )
            ) UNION
            (SELECT * FROM t_ses_ids_that_email_pass_auth_success_with_device_remembered)
        )
    )
),

t_mfa_attempt_success AS (
    (SELECT * FROM t_email_attempt_success)
    INTERSECT
    (
        SELECT * FROM (
            (
                SELECT * FROM (
                    (SELECT * FROM t_ses_ids_mfa_visit)
                    INTERSECT
                    (SELECT * FROM t_ses_ids_mfa_attempt_success)
                )
            ) UNION
            (SELECT * FROM t_ses_ids_that_email_pass_auth_success_with_device_remembered)
        )
    )
),

t_oidc_request AS (
    (SELECT * FROM t_email_attempt_success)
    INTERSECT
    (SELECT * FROM t_ses_ids_oidc_request_success)
    INTERSECT
    (
        SELECT * FROM (
            (
                SELECT * FROM (
                    (SELECT * FROM t_ses_ids_mfa_visit)
                    INTERSECT
                    (SELECT * FROM t_ses_ids_mfa_attempt_success)
                )
            ) UNION
            (SELECT * FROM t_ses_ids_that_email_pass_auth_success_with_device_remembered)
        )
    )
),

-- only has one OIDC requests success=true event in entire session
t_odic_requests_success_without_other_events AS (
    (SELECT * FROM t_ses_ids_oidc_request_success)
    EXCEPT
    (SELECT * FROM t_ses_ids_that_email_pass_auth_success)
    EXCEPT
    (SELECT * FROM t_ses_ids_mfa_attempt_success)
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
    (SELECT COUNT(*) FROM t_oidc_request) AS n_oidc_request
;
