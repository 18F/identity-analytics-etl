create schema if not exists public;
create table if not exists public.events_phone (
    id varchar(40) not null,
    visit_id varchar(40),
    visitor_id varchar(40),
    area_code varchar(10) not null,
    country_code varchar(10) not null,
    time timestamp
);