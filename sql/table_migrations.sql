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

  DROP TABLE events;
  ALTER TABLE events_tt RENAME TO events;
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
