CREATE GROUP enduserteam;
CREATE USER monfresh WITH password '$password';
ALTER GROUP enduserteam ADD USER monfresh;
GRANT USAGE ON SCHEMA "public" TO GROUP enduserteam;
GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO GROUP enduserteam;
