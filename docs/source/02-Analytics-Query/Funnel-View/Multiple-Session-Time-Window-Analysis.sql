/*
**Question**:

We observed that **many users use multiple sessions in single sign-up / authentication workflow**. This observation means:

1. user changed device or web browser in the workflow.
2. user made multiple attempts on different device or web browser.
3. the session timed out.

All of them potentially means poor user experience.

I want to figure out what's the impact and what is causing this.
*/


\set starttime '''2019-02-21'''
\set endtime '''2019-02-22'''

WITH E AS (
    SELECT
        events.user_id AS user_id,
        events.visit_id AS ses_id,
        events.user_ip AS ip_address,
        events.visitor_id AS visitor_id,
        events.user_agent AS user_agent,
        events.time AS time
    FROM events
    WHERE
        events.time BETWEEN :starttime AND :endtime
        AND events.service_provider IS NOT NULL
        AND events.service_provider != ''
),


t_user_id_with_one_session_id AS (
    SELECT
        E.user_id
    FROM E
    GROUP BY E.user_id
    HAVING
        COUNT(DISTINCT(E.ses_id)) = 1
        AND (max(E.time) - min(E.time)) <= 300000000
),


-- number of single user_id time window but have at least 2 sessions
-- reason could be multi ip, visitor_id, user_agent
t_user_id_with_multi_session_id AS (
    SELECT
        E.user_id,
        (COUNT(DISTINCT(E.ip_address)) >= 2) AS multi_ip,
        (COUNT(DISTINCT(E.visitor_id)) >= 2) AS multi_visitor_id,
        (COUNT(DISTINCT(E.user_agent)) >= 2) AS multi_user_agent
    FROM E
    GROUP BY E.user_id
    HAVING
        COUNT(DISTINCT(E.ses_id)) >= 2
        AND (max(E.time) - min(E.time)) <= 300000000
),


t_user_id_with_multi_session_id_extended AS (
    SELECT
        T.user_id,
        T.multi_ip,
        T.multi_visitor_id,
        T.multi_user_agent,
        (T.multi_ip AND T.multi_visitor_id) AS multi_ip_and_visitor_id,
        (T.multi_ip AND T.multi_user_agent) AS multi_ip_and_user_agent,
        (T.multi_visitor_id AND T.multi_user_agent) AS multi_visitor_id_and_user_agent,
        (T.multi_ip AND T.multi_visitor_id AND T.multi_user_agent) AS multi_all_three
    FROM t_user_id_with_multi_session_id T
),


t_n_time_window AS (
    SELECT
        (SELECT COUNT(t_user_id_with_one_session_id.user_id) FROM t_user_id_with_one_session_id) AS n_time_window_with_one_ses,
        COUNT(T.user_id) AS n_time_window_with_multi_ses,
        SUM(T.multi_ip::integer) AS n_multi_ip,
        SUM(T.multi_visitor_id::integer) AS n_multi_visitor_id,
        SUM(T.multi_user_agent::integer) AS n_multi_user_agent,
        SUM(T.multi_ip_and_visitor_id::integer) AS n_multi_ip_and_visitor_id,
        SUM(T.multi_ip_and_user_agent::integer) AS n_multi_ip_and_user_agent,
        SUM(T.multi_visitor_id_and_user_agent::integer) AS n_multi_visitor_id_and_user_agent,
        SUM(T.multi_all_three::integer) AS n_multi_all_three
    FROM t_user_id_with_multi_session_id_extended T
),


t_n_time_window_result_tmp AS (
    SELECT
        T.n_time_window_with_one_ses,
        T.n_time_window_with_multi_ses,
        T.n_multi_ip,
        T.n_multi_visitor_id,
        T.n_multi_user_agent,
        T.n_multi_ip_and_visitor_id,
        T.n_multi_ip_and_user_agent,
        T.n_multi_visitor_id_and_user_agent,
        -- passively change session reasons venn diagram
        (T.n_multi_ip + T.n_multi_user_agent + T.n_multi_user_agent - T.n_multi_ip_and_visitor_id - T.n_multi_ip_and_user_agent - T.n_multi_visitor_id_and_user_agent + T.n_multi_all_three) AS n_time_window_with_multi_ses,
        (T.n_multi_ip - T.n_multi_ip_and_visitor_id - T.n_multi_ip_and_user_agent + T.n_multi_all_three) AS n_multi_ip_only,
        (T.n_multi_visitor_id - T.n_multi_ip_and_visitor_id - T.n_multi_visitor_id_and_user_agent + T.n_multi_all_three) AS n_multi_visitor_id_only,
        (T.n_multi_user_agent - T.n_multi_ip_and_user_agent - T.n_multi_visitor_id_and_user_agent + T.n_multi_all_three) AS n_multi_user_agent_only,
        (T.n_multi_ip_and_visitor_id - T.n_multi_all_three) AS n_multi_ip_and_visitor_id_only,
        (T.n_multi_ip_and_user_agent - T.n_multi_all_three) AS n_multi_ip_and_user_agent_only,
        (T.n_multi_visitor_id_and_user_agent - T.n_multi_all_three) AS n_multi_visitor_id_and_user_agent_only,
        T.n_multi_all_three
    FROM t_n_time_window T
)


SELECT * FROM t_n_time_window_result_tmp LIMIT 100
--SELECT COUNT(*) FROM t_user_id_with_one_session_id
;
