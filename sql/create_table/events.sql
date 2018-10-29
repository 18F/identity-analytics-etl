create schema if not exists public;

create table if not exists public.events (
    id varchar(40) not null,
    name varchar(255) not null,
    user_agent varchar(4096),
    user_id varchar(40),
    user_ip varchar(50),
    host varchar(255),
    visit_id varchar(40),
    visitor_id varchar(40),
    time timestamp,
    event_properties varchar(4096),
    success boolean,
    existing_user boolean,
    otp_method varchar(20),
    context varchar(20),
    method varchar(20),
    authn_context varchar(50),
    service_provider varchar(255),
    loa3 boolean,
    active_profile boolean,
    errors varchar(4096)
)
sortkey (time);
