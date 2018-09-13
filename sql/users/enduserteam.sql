CREATE GROUP enduserteam;
CREATE USER monfresh WITH password '$password'; # change $password to specific
ALTER GROUP enduserteam ADD USER monfresh;
GRANT USAGE ON SCHEMA "public" TO GROUP enduserteam;
GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO GROUP enduserteam;
CREATE USER ericmill WITH password '$my_password'; 
ALTER GROUP enduserteam ADD USER ericmill;
