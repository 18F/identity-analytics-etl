CREATE VIEW password_success_rate
as (
      SELECT SUM(success::integer)/COUNT(*)::float as success_rate,
      date_trunc('hour', time) as hour
      FROM events
      WHERE name = 'Email and Password Authentication'
      GROUP BY hour
    );

CREATE VIEW mfa_success_rate
as (
      SELECT SUM(success::integer)/COUNT(*)::float as success_rate,
      date_trunc('hour', time) as hour
      FROM events
      WHERE name = 'Multi-Factor Authentication: max attempts reached'
      GROUP BY hour
    );

CREATE VIEW experience_durations AS (
  WITH tj as (
    SELECT 
      t1.name as t1_name, 
      t2.name as t2_name, 
      t1.user_id as t1_user_id, 
      t1.visit_id as t1_visit_id, 
      EXTRACT(epoch FROM (t2.time - t1.time)) AS duration,
      t1.time as time 
    FROM events t1 
    JOIN events t2 
    ON 
      t1.user_id = t2.user_id 
    AND 
      t1.visit_id = t2.visit_id
    WHERE EXTRACT(epoch FROM (t2.time - t1.time)) > 0
  )
  SELECT q.exp_name,q.duration,q.time FROM
  (
      SELECT 
        'email submission' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User Registration: enter email visited' 
      AND tj.t2_name = 'User Registration: Email Submitted' 
    UNION
      SELECT 
        'phone setup' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User Registration: phone setup visited' 
      AND tj.t2_name = 'User Registration: personal key visited' 
    UNION
      SELECT 
        'agency handoff' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User registration: agency handoff visited' 
      AND tj.t2_name = 'User registration: agency handoff complete' 
  ) q
);

CREATE VIEW experience_durations_visitor_id AS (
  WITH tj as (
    SELECT 
      t1.name as t1_name, 
      t2.name as t2_name, 
      t1.user_id as t1_user_id, 
      t1.visitor_id as t1_visitor_id, 
      EXTRACT(epoch FROM (t2.time - t1.time)) AS duration,
      t1.time as time 
    FROM events t1 
    JOIN events t2 
    ON 
      t1.user_id = t2.user_id 
    AND 
      t1.visitor_id = t2.visitor_id
    WHERE EXTRACT(epoch FROM (t2.time - t1.time)) > 0
  )
  SELECT q.exp_name,q.duration,q.time FROM
  (
      SELECT 
        'email submission' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User Registration: enter email visited' 
      AND tj.t2_name = 'User Registration: Email Submitted' 
    UNION
      SELECT 
        'phone setup' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User Registration: phone setup visited' 
      AND tj.t2_name = 'User Registration: personal key visited' 
    UNION
      SELECT 
        'agency handoff' AS exp_name, 
        duration, 
        tj.time as time
      FROM tj 
      WHERE tj.t1_name = 'User registration: agency handoff visited' 
      AND tj.t2_name = 'User registration: agency handoff complete' 
  ) q
);

CREATE VIEW daily_active_users AS
(SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "time"
   FROM events
  GROUP BY events."time"::date);

CREATE VIEW hourly_active_users AS
(SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "day", pgdate_part('hour'::text, events."time") AS hr
   FROM events
  GROUP BY events."time"::date, pgdate_part('hour'::text, events."time"));

