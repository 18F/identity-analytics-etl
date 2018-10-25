create schema if not exists public;
create table if not exists public.service_providers (
    events_sp varchar(255),
    service_provider varchar(255)
);
