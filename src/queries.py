class Queries:

    def __init__(self):
        self.create_events = """CREATE TABLE events (
                                  id VARCHAR(40) NOT NULL,
                                  name VARCHAR(255) NOT NULL,
                                  user_agent VARCHAR(255),
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
                                  errors VARCHAR(4096),

                                  PRIMARY KEY(id));"""

        self.drop_events = """DROP TABLE events;"""

        self.create_uploaded_files = """CREATE TABLE uploaded_files (
                                        s3filename VARCHAR(100) NOT NULL,
                                        destination VARCHAR(100) NOT NULL,
                                        uploaded_at TIMESTAMP,

                                        PRIMARY KEY(s3filename,destination));"""

        self.drop_uploaded_files = """DROP TABLE uploaded_files;"""

        self.create_pageviews = """CREATE TABLE pageviews (
                                    method VARCHAR(10) NOT NULL,
                                    path VARCHAR(1024),
                                    format VARCHAR(15),
                                    controller VARCHAR(100),
                                    action VARCHAR(15),
                                    status SMALLINT,
                                    duration FLOAT,
                                    user_id VARCHAR(40),
                                    user_agent VARCHAR(255),
                                    ip VARCHAR(50),
                                    host VARCHAR(255),
                                    timestamp TIMESTAMP,
                                    uuid VARCHAR(40) NULL UNIQUE,

                                    PRIMARY KEY(path, ip, timestamp)
                                  );"""

        self.drop_pageviews = """DROP TABLE pageviews;"""

        self.create_user_agents = """CREATE TABLE user_agents (
                                        user_agent VARCHAR(255) NOT NULL,
                                        browser VARCHAR(100),
                                        platform VARCHAR(100),
                                        version VARCHAR(100),

                                        PRIMARY KEY(user_agent)
                                      );"""

        self.drop_user_agents = """DROP TABLE user_agents;"""

if __name__ == '__main__':
    q = Queries()
    print(q.create_user_agents)
