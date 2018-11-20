# Redshift Queries

This is a list of queries that are best suited to obtain from Redshift

## Accessing the Redshift psql console

## Metrics

### How many unique users have used the remember me feature?
Event name: "Email and Password Authentication"
event_properties['remember_device'] = true.
For each user, only count the event once.

### What are the most used 2FA methods?
Event name: "Multi-Factor Authentication" (exact match)
event_properties['context'] = 'authentication'
event_properties['success'] = true

Then calculate percentages of each `multi_factor_auth_method` event property.
Possible values are: `sms`, `voice`, `totp` (refers to authentication app),
`piv_cac`, `webauthn` (refers to hardware security key), and `personal key`.

It might also make sense to only count unique events per user so that if
a few users are generating a disproportionate amount of events, it doesn't skew
the results.
