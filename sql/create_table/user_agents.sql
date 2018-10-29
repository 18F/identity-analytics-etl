create schema if not exists public;
create table if not exists public.user_agents (
    user_agent varchar(255),
    browser varchar(100),
    platform varchar(100),
    version varchar (100)
);

