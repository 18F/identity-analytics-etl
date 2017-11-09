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
