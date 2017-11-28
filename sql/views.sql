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

CREATE VIEW experience_durations AS
  (SELECT 'email submission' AS exp_name, duration, t.time FROM
    (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
      EXTRACT(epoch FROM (t2.time - t1.time)) AS duration, t1.time as time
      FROM events t1 JOIN events t2
      ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
      WHERE t1.name = 'User Registration: enter email visited'
      AND t2.name = 'User Registration: Email Submitted') t
    WHERE t.duration > 0
    UNION
    SELECT 'phone setup' AS exp_name, duration, t2.time FROM
      (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
        EXTRACT(epoch FROM(t2.time - t1.time)) AS duration, t1.time AS time
        FROM events t1 JOIN events t2
        ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
        WHERE t1.name = 'User Registration: phone setup visited'
        AND t2.name = 'User Registration: personal key visited') t2
    WHERE t2.duration > 0
    UNION
    SELECT 'agency handoff' AS exp_name, duration, t3.time FROM
      (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
        EXTRACT(epoch FROM (t2.time - t1.time)) AS duration, t1.time AS time
        FROM events t1 JOIN events t2
        ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
        WHERE t1.name = 'User registration: agency handoff visited'
        AND t2.name = 'User registration: agency handoff complete') t3
      WHERE t3.duration > 0);

 CREATE VIEW experience_durations AS
    (SELECT 'email submission' AS exp_name, duration, t.time FROM
      (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
        EXTRACT(epoch FROM (t2.time - t1.time)) AS duration, t1.time as time
        FROM events t1 JOIN events t2
        ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
        WHERE t1.name = 'User Registration: enter email visited'
        AND t2.name = 'User Registration: Email Submitted') t
      WHERE t.duration > 0
      UNION
      SELECT 'phone setup' AS exp_name, duration, t2.time FROM
        (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
          EXTRACT(epoch FROM(t2.time - t1.time)) AS duration, t1.time AS time
          FROM events t1 JOIN events t2
          ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
          WHERE t1.name = 'User Registration: phone setup visited'
          AND t2.name = 'User Registration: personal key visited') t2
      WHERE t2.duration > 0
      UNION
      SELECT 'agency handoff' AS exp_name, duration, t3.time FROM
        (SELECT t1.name, t2.name, t1.user_id, t1.visit_id,
          EXTRACT(epoch FROM (t2.time - t1.time)) AS duration, t1.time AS time
          FROM events t1 JOIN events t2
          ON t1.user_id = t2.user_id AND t1.visit_id = t2.visit_id
          WHERE t1.name = 'User registration: agency handoff visited'
          AND t2.name = 'User registration: agency handoff complete') t3
        WHERE t3.duration > 0);


  CREATE VIEW experience_durations_visitor_id AS
    ( SELECT 'email submission' AS exp_name, t.duration, t."time"
   FROM ( SELECT t1.name, t2.name, t1.user_id, t1.visitor_id, "date_part"('epoch'::text, t2."time" - t1."time") AS duration, t1."time"
           FROM events t1
      JOIN events t2 ON t1.user_id::text = t2.user_id::text AND t1.visitor_id::text = t2.visitor_id::text
     WHERE t1.name::text = 'User Registration: enter email visited'::text AND t2.name::text = 'User Registration: Email Submitted'::text) t
  WHERE t.duration > 0::double precision
  UNION
  SELECT 'phone setup' AS exp_name, t2.duration, t2."time"
   FROM ( SELECT t1.name, t2.name, t1.user_id, t1.visitor_id, "date_part"('epoch'::text, t2."time" - t1."time") AS duration, t1."time"
           FROM events t1
      JOIN events t2 ON t1.user_id::text = t2.user_id::text AND t1.visitor_id::text = t2.visitor_id::text
     WHERE t1.name::text = 'User Registration: phone setup visited'::text AND t2.name::text = 'User Registration: personal key visited'::text) t2
  WHERE t2.duration > 0::double precision)
  UNION
  SELECT 'agency handoff' AS exp_name, t3.duration, t3."time"
   FROM ( SELECT t1.name, t2.name, t1.user_id, t1.visitor_id, "date_part"('epoch'::text, t2."time" - t1."time") AS duration, t1."time"
           FROM events t1
      JOIN events t2 ON t1.user_id::text = t2.user_id::text AND t1.visitor_id::text = t2.visitor_id::text
     WHERE t1.name::text = 'User registration: agency handoff visited'::text AND t2.name::text = 'User registration: agency handoff complete'::text) t3
  WHERE t3.duration > 0::double precision;

CREATE VIEW daily_active_users AS
(SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "time"
   FROM events
  GROUP BY events."time"::date);

CREATE VIEW hourly_active_users AS
(SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "day", pgdate_part('hour'::text, events."time") AS hr
   FROM events
  GROUP BY events."time"::date, pgdate_part('hour'::text, events."time"));

