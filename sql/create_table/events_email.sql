create schema if not exists public;
create table if not exists public.events_email (
    id varchar(40) not null,
    name varchar(255) not null,
    domain_name varchar(255),
    time timestamp
);