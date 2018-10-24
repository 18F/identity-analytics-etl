create schema if not exists public;
create table if not exists public.pageviews (
    method varchar(10) not null,
    path varchar(1024),
    format varchar(255),
    controller varchar (100),
    action varchar(30),
    status smallint,
    duration float8,
    user_id varchar(80),
    user_agent varchar(4096),
    ip varchar(80),
    host varchar(255),
    timestamp timestamp,
    uuid varchar(80) not null
)
sortkey (timestamp);

