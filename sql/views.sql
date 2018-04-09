-- Postgres alias for Redshift GETDATE() 
CREATE OR REPLACE FUNCTION GETDATE() 
RETURNS timestamp AS $$
DECLARE
  dt timestamp;  
BEGIN
  SELECT NOW() at time zone 'UTC' INTO dt;
  RETURN dt;
END;
$$ LANGUAGE plpgsql;

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
    AND t1.time::date >= (DATEADD(month, -1, GETDATE()) at time zone 'UTC') 
    AND t2.time::date >= (DATEADD(month, -1, GETDATE()) at time zone 'UTC') 
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
    AND t1.time::date >= (DATEADD(month, -1, GETDATE()) at time zone 'UTC')  
    AND t2.time::date >= (DATEADD(month, -1, GETDATE()) at time zone 'UTC')
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
(
  SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "time"
  FROM events
  WHERE events."time"::date >= (GETDATE() - interval '30' day) 
  GROUP BY events."time"::date
);

CREATE VIEW hourly_active_users AS
(
  SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "day", date_part('hour', events."time")::text AS hr
  FROM events
  WHERE events."time"::date >= (GETDATE() - interval '30' day) 
  GROUP BY events."time"::date, date_part('hour', events."time")::text
);

CREATE VIEW monthly_signups AS (
  SELECT 
    e.month,
    count(e.c_uid) AS count 
    FROM (
    SELECT 
    date_trunc(('month'), i.time) as month, 
    i.user_id AS c_uid  
    FROM 
    (
       SELECT events.user_id as user_id, 
       events.time as time, 
       ROW_NUMBER() OVER (PARTITION BY events.user_id ORDER BY events.time ASC) AS uid_ranked
       FROM events
    ) i 
    WHERE i.uid_ranked = 1 
  ) e group by e.month ORDER BY e.month asc
);


CREATE VIEW avg_daily_signups_by_month AS (
  SELECT 
  ed.month as month, 
  avg(ed.d_count) avg_daily_signups 
  FROM (
    SELECT 
      e.day,
      date_trunc(('month'), e.day) as month,
      count(e.c_uid) AS d_count 
      FROM (
      SELECT 
      date_trunc(('day'), i.time) as day, 
      i.user_id AS c_uid  
      FROM 
      (
         SELECT events.user_id as user_id, 
         events.time as time, 
         ROW_NUMBER() OVER (PARTITION BY events.user_id ORDER BY events.time ASC) AS uid_ranked
         FROM events
      ) i 
      WHERE i.uid_ranked = 1 
    ) e group by e.day ORDER BY e.day asc 
  ) ed group by ed.month ORDER BY ed.month asc
);



