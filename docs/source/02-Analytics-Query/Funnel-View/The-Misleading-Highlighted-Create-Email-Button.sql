/*
**Question**:

We observed that some users clicked ``Create Account`` button (Sign in page) https://secure.login.gov/sign_up/start?request_id=xxx) and ends with Sign in workflow.

As business person, I want to figure out how many users been misled by the Highlighted ``Create Account`` Button.

**SQL Description**:

1. P(A): t_ses_id_email_pass_auth gives us sessions trying to sign in.
2. P(B): t_ses_id_mfa_success gives us sessions trying to finish MFA sign in.
3. P(C): t_ses_id_submitted_email_then_sign_in gives us sessions clicked ``Create Account`` button before they land to sign in page.

Then we can easily derive:

1. P(C|A)
2. P(C|B)
*/

\set starttime '''2019-01-01'''
\set endtime '''2019-02-01'''


WITH E AS (
    SELECT
        events.name AS name,
        events.time AS time,
        events.visit_id AS ses_id,
        events.event_properties AS event_properties,
        events.success AS success
    FROM events
    WHERE
        events.time BETWEEN :starttime AND :endtime
        AND events.service_provider IS NOT NULL
        AND events.service_provider != ''
),

-- sessions that made email password login attempts
t_ses_id_email_pass_auth AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE E.name = 'Email and Password Authentication'
),


-- sessions that made MFA login attempts
t_ses_id_mfa_success AS (
    SELECT
        DISTINCT(E.ses_id) AS ses_id
    FROM E
    WHERE
        E.name = 'Multi-Factor Authentication'
        AND E.success IS TRUE
),


-- Find out sessions that clicked "Create Account" before sign in attempt
t_min_time_by_ses_id_and_name AS (
    SELECT
        E.ses_id,
        E.name,
        min(E.time) AS time
    FROM E
    WHERE
        E.name = 'User Registration: Email Submitted'
        OR E.name = 'Email and Password Authentication'
    GROUP BY E.ses_id, E.name
    ORDER BY E.ses_id
),


t_ses_id_submitted_email_then_sign_in AS (
    SELECT T1.ses_id
    FROM (
        SELECT
            T.ses_id,
            T.name,
            T.time,
            rank() OVER (PARTITION BY T.ses_id ORDER BY T.time) AS nth_event
        FROM t_min_time_by_ses_id_and_name T
    ) T1
    WHERE
        T1.nth_event = 1 AND T1.name = 'User Registration: Email Submitted'
),


-- sessions that made sign in attempts, and clicked "Create Account" button
t_ses_id_email_pass_auth_but_submit_email_first AS (
    (SELECT * FROM t_ses_id_email_pass_auth)
    INTERSECT
    (SELECT * FROM t_ses_id_submitted_email_then_sign_in)
),


-- sessions that finished MFA sign in, and clicked "Create Account" button
t_ses_id_mfa_success_but_submit_email_first AS (
    (SELECT * FROM t_ses_id_mfa_success)
    INTERSECT
    (SELECT * FROM t_ses_id_submitted_email_then_sign_in)
),


-- organize output
t_result_tmp AS (
    SELECT
        (SELECT COUNT(*) FROM t_ses_id_email_pass_auth) AS n_email_pass_auth,
        (SELECT COUNT(*) FROM t_ses_id_email_pass_auth_but_submit_email_first) AS n_email_pass_auth_but_submit_email_first,
        (SELECT COUNT(*) FROM t_ses_id_mfa_success) AS n_mfa_success,
        (SELECT COUNT(*) FROM t_ses_id_mfa_success_but_submit_email_first) AS n_mfa_success_but_submit_email_first
)


SELECT
    (T.n_email_pass_auth_but_submit_email_first * 100.0 / T.n_email_pass_auth) AS misled_perc_on_sign_in_attempt_users,
    (T.n_mfa_success_but_submit_email_first * 100.0 / T.n_mfa_success) AS misled_perc_on_sign_in_success_users
FROM t_result_tmp T
;
