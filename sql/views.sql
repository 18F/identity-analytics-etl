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


CREATE VIEW email_domain_return_rate AS
SELECT ( (count(DISTINCT t.u2))::double precision / (count(DISTINCT t.u1))::double precision) AS return_rate,
       count(*) AS raw_count,
       (t.time1)::date AS time1,
       t.domain_name
FROM
  ( SELECT e2.user_id AS u2,
           e.user_id AS u1,
           e2.name,
           ee.name,
           e."time" AS time1,
           e2."time" AS time2,
           ee.domain_name
   FROM ( (events_email ee
           JOIN EVENTS e ON (((e.id)::text = (ee.id)::text)))
         LEFT JOIN
           ( SELECT events.id,
                    events.name,
                    events.user_agent,
                    events.user_id,
                    events.user_ip,
                    events."host",
                    events.visit_id,
                    events.visitor_id,
                    events."time",
                    events.event_properties,
                    events.success,
                    events.existing_user,
                    events.otp_method,
                    events.context,
                    events.method,
                    events.authn_context,
                    events.service_provider,
                    events.loa3,
                    events.active_profile,
                    events.errors
            FROM EVENTS
            WHERE ( (events.name)::text = 'Email Confirmation'::text) ) e2 ON (((e2.user_id)::text = (e.user_id)::text)))
   WHERE (((((date_diff('days'::text, ((e2."time")::date)::TIMESTAMP WITHOUT TIME ZONE, ((e."time")::date)::TIMESTAMP WITHOUT TIME ZONE) < 2)
             OR (e2."time" IS NULL))
            AND ((e.user_id)::text <> 'anonymous-uuid'::text))
           AND ((e."time")::date > '2018-01-01'::date))
          AND (((((((ee.domain_name)::text = 'gmail.com'::text)
                   OR ((ee.domain_name)::text = 'yahoo.com'::text))
                  OR ((ee.domain_name)::text = 'aol.com'::text))
                 OR ((ee.domain_name)::text = 'hotmail.com'::text))
                OR ((ee.domain_name)::text = 'comcast.net'::text))
               OR ((ee.domain_name)::text = 'verizon.net'::text)))) t
GROUP BY t.domain_name,
         (t.time1)::date
ORDER BY (t.time1)::date DESC;



CREATE VIEW return_rate AS
SELECT ( (count(DISTINCT derived_table1.v2))::double precision / (count(DISTINCT derived_table1.v1))::double precision) AS return_rate,
       count(*) AS raw_count,
       derived_table1.time1,
       derived_table1.service_provider
FROM
  ( SELECT e2.user_id AS v2,
           e.user_id AS v1,
           e2.name,
           e.name,
           (e."time")::date AS time1,
           (e2."time")::date AS time2,
           sp.service_provider
   FROM ( (EVENTS e
           LEFT JOIN
             (SELECT events.id,
                     events.name,
                     events.user_agent,
                     events.user_id,
                     events.user_ip,
                     events."host",
                     events.visit_id,
                     events.visitor_id,
                     events."time",
                     events.event_properties,
                     events.success,
                     events.existing_user,
                     events.otp_method,
                     events.context,
                     events.method,
                     events.authn_context,
                     events.service_provider,
                     events.loa3,
                     events.active_profile,
                     events.errors
              FROM EVENTS
              WHERE ((events.name)::text = 'User registration: agency handoff complete'::text)) e2 ON (((e.user_id)::text = (e2.user_id)::text)))
         LEFT JOIN service_providers sp ON (((e.service_provider)::text = (sp.events_sp)::text)))
   WHERE ((((e.name)::text = 'User Registration: Email Submitted'::text)
           AND ((e.user_id)::text <> 'anonymous-uuid'::text))
          AND ((date_diff('hours'::text, e2."time", e."time") < 2)
               OR (e2."time" IS NULL)))) derived_table1
GROUP BY derived_table1.service_provider,
         derived_table1.time1
ORDER BY derived_table1.time1 DESC;

