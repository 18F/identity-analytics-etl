-- https://dba.stackexchange.com/a/156850

CREATE GROUP view_only_group;

CREATE USER dashboarduser WITH password $password;

ALTER GROUP view_only_group ADD USER dashboarduser;

GRANT USAGE ON SCHEMA "public" TO GROUP view_only_group;

GRANT SELECT ON ALL TABLES IN SCHEMA "public" TO GROUP view_only_group;
