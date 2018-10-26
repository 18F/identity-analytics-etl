create schema if not exists public;
create table if not exists public.events_devices (
    id varchar(40) not null,
    name varchar(255) not null,
    user_agent varchar(4096),
    browser_name varchar(255),
    browser_version varchar(255),
    browser_platform_name varchar(255),
    browser_platform_version varchar(255),
    browser_device_name varchar(255),
    browser_device_typed varchar(255),
    browser_bot boolean,
    time timestamp
);