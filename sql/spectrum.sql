-- Schema for Spectrum tables.
-- NOTE: TIMESTAMP fields are stored as VARCHAR. 

drop table spectrum.events;
create external table spectrum.events(
    id VARCHAR(40),
    name VARCHAR(255),
    user_agent VARCHAR(4096),
    user_id VARCHAR(40),
    user_ip VARCHAR(50),
    host VARCHAR(255),
    visit_id VARCHAR(40),
    visitor_id VARCHAR(40),
    time VARCHAR(64),
    event_properties VARCHAR(4096),
    success BOOLEAN,
    existing_user BOOLEAN,
    otp_method VARCHAR(20),
    context VARCHAR(20),
    method VARCHAR(20),
    authn_context VARCHAR(50),
    service_provider VARCHAR(255),
    loa3 BOOLEAN,
    active_profile BOOLEAN,
    errors VARCHAR(4096)
)
database 'spectrumdb' 
stored as parquet
location 's3://login-gov-prod-analytics-parquet/events';

DROP TABLE IF EXISTS spectrum.pageviews;
CREATE EXTERNAL TABLE spectrum.pageviews (
    method VARCHAR(10),
    path VARCHAR(1024),
    format VARCHAR(255),
    controller VARCHAR(100),
    action VARCHAR(15),
    status BIGINT,
    duration FLOAT,
    user_id VARCHAR(40),
    user_agent VARCHAR(4096),
    ip VARCHAR(50),
    host VARCHAR(255),
    uuid VARCHAR(64),
    timestamp VARCHAR(64)
)
database 'spectrumdb' 
stored as parquet
location 's3://login-gov-prod-analytics-parquet/pageviews';

DROP TABLE IF EXISTS spectrum.events_email;
CREATE TABLE spectrum.events_email (
    id VARCHAR(40),
    name VARCHAR(255),
    domain_name VARCHAR(255),
    time VARCHAR(64)
)
database 'spectrumdb' 
stored as parquet
location 's3://login-gov-prod-analytics-parquet/events_email';

DROP TABLE IF EXISTS spectrum.events_devices;
CREATE TABLE spectrum.events_devices (
    id VARCHAR(40),
    name VARCHAR(255),
    user_agent VARCHAR(4096),
    browser_name VARCHAR(255),
    browser_version VARCHAR(255),
    browser_platform_name VARCHAR(255),
    browser_platform_version VARCHAR(255),
    browser_device_name VARCHAR(255),
    browser_device_type VARCHAR(255),
    browser_bot BOOLEAN,
    time VARCHAR(64)
)
database 'spectrumdb' 
stored as parquet
location 's3://login-gov-prod-analytics-parquet/events_devices';
