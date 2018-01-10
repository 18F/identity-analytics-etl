BEGIN;
  DROP TABLE IF EXISTS events_tt;
  CREATE TABLE events_tt (
    id VARCHAR(40) NOT NULL,
    name VARCHAR(255) NOT NULL,
    user_agent VARCHAR(4096),
    user_id VARCHAR(40),
    user_ip VARCHAR(50),
    host VARCHAR(255),
    visit_id VARCHAR(40),
    visitor_id VARCHAR(40),
    time TIMESTAMP,
    event_properties VARCHAR(4096),

    success BOOLEAN,
    existing_user BOOLEAN,
    otp_method VARCHAR(20),
    context VARCHAR(20),
    method VARCHAR(20),
    authn_context VARCHAR(50),
    service_provider VARCHAR(255),
    loa3 BOOLEAN,
    active_profile BOOLEAN,
    errors VARCHAR(4096))
    SORTKEY(time);

  INSERT INTO events_tt (SELECT * FROM events);

  DROP VIEW experience_durations;
  DROP VIEW experience_durations_visitor_id;
  DROP VIEW daily_active_users;
  DROP VIEW hourly_active_users;

  DROP TABLE events;
  ALTER TABLE events_tt RENAME TO events;

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
    AND t1."time"::date >= (GETDATE() at time zone 'UTC' - interval '1' month)  
    AND t2."time"::date >= (GETDATE() at time zone 'UTC' - interval '1' month)
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
    AND t1.time::date >= (GETDATE() at time zone 'UTC' - interval '1' month)  
    AND t2.time::date >= (GETDATE() at time zone 'UTC' - interval '1' month)
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
  WHERE events."time"::date >= (GETDATE() at time zone 'UTC' - interval '30' day)
  GROUP BY events."time"::date
);

CREATE VIEW hourly_active_users AS
(
  SELECT count(DISTINCT events.user_id) AS count, events."time"::date AS "day", date_part('hour', events."time")::text AS hr
  FROM events
  WHERE events."time"::date >= (GETDATE() at time zone 'UTC' - interval '30' day)
  GROUP BY events."time"::date, date_part('hour', events."time")::text
);

END;

BEGIN;
  DROP TABLE IF EXISTS pageviews_tt;
  CREATE TABLE pageviews_tt (
    method VARCHAR(10) NOT NULL,
    path VARCHAR(1024),
    format VARCHAR(255),
    controller VARCHAR(100),
    action VARCHAR(15),
    status SMALLINT,
    duration FLOAT,
    user_id VARCHAR(40),
    user_agent VARCHAR(4096),
    ip VARCHAR(50),
    host VARCHAR(255),
    timestamp TIMESTAMP,
    uuid VARCHAR(64) NOT NULL
    )
    SORTKEY(timestamp);

    INSERT INTO pageviews_tt (SELECT * FROM pageviews);

    DROP TABLE pageviews;
    ALTER TABLE pageviews_tt RENAME TO pageviews;
END;
