# Login.gov IdP Analytics

This documents the events captured by the [identity-idp](https://github.com/18F/identity-idp) app.

## Where to find the raw event logs
- In the `/srv/idp/current/log/events.log` path on any of our current IdP servers.
- In the `login-gov-prod-logs/elk` S3 bucket.

## How to add an event in the IdP app (audience: developers)
Whenever possible, use the same event to track its various states.
For example, when a user enters their email address when creating an account,
various things can result from this action:

- the email address is valid
- the email address is invalid
- the email address already exists in the database

Instead of using conditional statements in a controller to call a different
event for each possible outcome, you would capture the event-specific properties
up front once, then pass them in to a single event. This makes it easier to
query the total registration attempts, while also making it easy to get
percentages of invalid vs valid attempts, for example.

Another thing to think about is whether multiple events have a common theme that
would be better represented as a single event. For example, when a user sets up
two-factor authentication, it might seem sensible to create separate events for
each type of 2FA method (phone, authentication app, security key, PIV/CAC).
However, this makes it harder to make more general queries such as "how many
users have set up 2FA?". To make that easier to answer, a single event called
"2FA Setup" would be preferable, and the various options could be captured as
event properties in a field called `two_factor_method` for example.

## Making changes to event properties
Before making a change, please discuss it with the analytics team. Changing
names of existing properties can impact the queries we make.

## Event Structure
Events are stored in JSON format in `events.log`. Here is an example:
```json
{
  "name": "Email and Password Authentication",
  "properties": {
    "event_properties": {
      "success": true,
      "user_locked_out": false,
      "stored_location": null,
      "sp_request_url_present": false,
      "remember_device": true
    },
    "user_id": "86a59d2b-0dec-4716-bb46-a674d9def066",
    "user_ip": "::1",
    "host": "localhost",
    "pid": 72369,
    "service_provider": null,
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "browser_name": "Chrome",
    "browser_version": "70.0.3538.77",
    "browser_platform_name": "Mac",
    "browser_platform_version": "10.13.6",
    "browser_device_name": null,
    "browser_device_type": "desktop",
    "browser_bot": false
  },
  "time": "2018-11-08T17:09:26.411Z",
  "id": "efe2c962-a670-442a-9fb2-c8257ad9a3bf",
  "visitor_id": "1056d484-194c-4b8c-978d-0c0f57958f04",
  "visit_id": "863a0969-2f30-472b-a534-f302efad6881"
}
```
The top-level keys are:

- name: the name of the event
- time: the UTC timestamp of the event
- id: a unique id of the event
- visitor_id: a unique id that corresponds to the user's browser cookie
- visit_id: a unique id that is based on the session. It changes for every new session.
- properties: a hash with the following keys:
  - event_properties: a hash with event-specific properties
  - user_id: the user's unique UUID. If we don't know who the user is, the value
  will be `'anonymous-uuid'`
  - user_ip: the user's IP address
  - host: the FQDN of the server, such as `secure.login.gov`
  - pid: the Process ID (not relevant to analytics queries)
  - service_provider: the service provider the user came from, such as `urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD`. If the user
  visited the site directly, or their session expired, then this
  will be `null`.
  - user_agent: The full User Agent
  - browser_name: The name of the browser, such as `Chrome`
  - browser_version: The browser version, such as `70.0.3538.77`
  - browser_platform_name: The name of the OS, such as `Mac` or `Windows`
  - browser_platform_version: The OS version, such as `10.13.6`
  - browser_device_name: The name of the mobile device, such as `iPhone`
  - browser_device_type: The type of device, such as `smartphone`, `desktop`, and `tablet`.
  - browser_bot: Whether or not this user agent is considered a bot. `true` or `false`.

For more possible browser-related values, visit
[DeviceDetector](https://github.com/podigee/device_detector), the gem we user to
parse the user agent.

## Events

<!-- MarkdownTOC levels="3" autolink="true" bracket="round" -->

- [Definitions](#definitions)
- [Account Reset](#account-reset)
- [Account Deletion Requested](#account-deletion-requested)
- [Account deletion and reset visited](#account-deletion-and-reset-visited)
- [Doc Auth visited](#doc-auth-visited)
- [Doc Auth submitted](#doc-auth-submitted)
- [Email and Password Authentication](#email-and-password-authentication)
- [Email Change Request](#email-change-request)
- [Email Confirmation](#email-confirmation)
- [Frontend: Browser capabilities](#frontend-browser-capabilities)
- [IdV: basic info visited](#idv-basic-info-visited)
- [IdV: basic info form submitted](#idv-basic-info-form-submitted)
- [IdV: basic info vendor submitted](#idv-basic-info-vendor-submitted)
- [IdV: cancellation visited](#idv-cancellation-visited)
- [IdV: cancellation confirmed](#idv-cancellation-confirmed)
- [IdV: come back later visited](#idv-come-back-later-visited)
- [IdV: max attempts exceeded](#idv-max-attempts-exceeded)
- [IdV: final resolution](#idv-final-resolution)
- [IdV: forgot password visited](#idv-forgot-password-visited)
- [IdV: forgot password confirmed](#idv-forgot-password-confirmed)
- [IdV: intro visited](#idv-intro-visited)
- [IdV: jurisdiction visited](#idv-jurisdiction-visited)
- [IdV: jurisdiction form submitted](#idv-jurisdiction-form-submitted)
- [IdV: phone confirmation form](#idv-phone-confirmation-form)
- [IdV: phone confirmation vendor](#idv-phone-confirmation-vendor)
- [Idv: Phone OTP attempts rate limited](#idv-phone-otp-attempts-rate-limited)
- [Idv: Phone OTP rate limited user](#idv-phone-otp-rate-limited-user)
- [Idv: Phone OTP sends rate limited](#idv-phone-otp-sends-rate-limited)
- [IdV: phone confirmation otp resent](#idv-phone-confirmation-otp-resent)
- [IdV: phone confirmation otp sent](#idv-phone-confirmation-otp-sent)
- [IdV: phone confirmation otp submitted](#idv-phone-confirmation-otp-submitted)
- [IdV: phone confirmation otp visited](#idv-phone-confirmation-otp-visited)
- [IdV: Phone OTP Delivery Selection Submitted](#idv-phone-otp-delivery-selection-submitted)
- [IdV: Phone OTP delivery Selection Visited](#idv-phone-otp-delivery-selection-visited)
- [IdV: phone of record visited](#idv-phone-of-record-visited)
- [IdV: review complete](#idv-review-complete)
- [IdV: review info visited](#idv-review-info-visited)
- [IdV: verification attempt cancelled](#idv-verification-attempt-cancelled)
- [Invalid Authenticity Token](#invalid-authenticity-token)
- [Logout Initiated](#logout-initiated)
- [Multi-Factor Authentication](#multi-factor-authentication)
- [Multi-Factor Authentication: enter OTP visited](#multi-factor-authentication-enter-otp-visited)
- [Multi-Factor Authentication: enter personal key visited](#multi-factor-authentication-enter-personal-key-visited)
- [Multi-Factor Authentication: max attempts reached](#multi-factor-authentication-max-attempts-reached)
- [Multi-Factor Authentication: option list](#multi-factor-authentication-option-list)
- [Multi-Factor Authentication: option list visited](#multi-factor-authentication-option-list-visited)
- [Multi-Factor Authentication: phone setup](#multi-factor-authentication-phone-setup)
- [Multi-Factor Authentication: max otp sends reached](#multi-factor-authentication-max-otp-sends-reached)
- [OpenID Connect: bearer token authentication](#openid-connect-bearer-token-authentication)
- [OpenID Connect: authorization request](#openid-connect-authorization-request)
- [OpenID Connect: token](#openid-connect-token)
- [OTP: Delivery Selection](#otp-delivery-selection)
- [Password Changed](#password-changed)
- [Password Creation](#password-creation)
- [Password Max Attempts Reached](#password-max-attempts-reached)
- [Password Reset: Email Submitted](#password-reset-email-submitted)
- [Password Reset: Password Submitted](#password-reset-password-submitted)
- [Password Reset: Token Submitted](#password-reset-token-submitted)
- [Password Reset: Email Form Visited](#password-reset-email-form-visited)
- [Personal Key Viewed](#personal-key-viewed)
- [Phone Number Change: requested](#phone-number-change-requested)
- [Phone Number Deletion: requested](#phone-number-deletion-requested)
- [Profile Encryption: Invalid](#profile-encryption-invalid)
- [Profile: Created new personal key](#profile-created-new-personal-key)
- [Rate Limit Triggered](#rate-limit-triggered)
- [Response Timed Out](#response-timed-out)
- [SAML Auth](#saml-auth)
- [Session Timed Out](#session-timed-out)
- [Sign in page visited](#sign-in-page-visited)
- [TOTP Setup](#totp-setup)
- [TOTP Setup Visited](#totp-setup-visited)
- [TOTP: User Disabled TOTP](#totp-user-disabled-totp)
- [Twilio Phone Validation Failed](#twilio-phone-validation-failed)
- [Twilio SMS Inbound Message Received](#twilio-sms-inbound-message-received)
- [Twilio SMS Inbound Validation Failed](#twilio-sms-inbound-validation-failed)
- [User registration: agency handoff visited](#user-registration-agency-handoff-visited)
- [User registration: agency handoff complete](#user-registration-agency-handoff-complete)
- [User Registration: Email Submitted](#user-registration-email-submitted)
- [User Registration: Email Confirmation](#user-registration-email-confirmation)
- [User Registration: Email Confirmation requested due to invalid token](#user-registration-email-confirmation-requested-due-to-invalid-token)
- [User Registration: enter email visited](#user-registration-enter-email-visited)
- [User Registration: intro visited](#user-registration-intro-visited)
- [User Registration: 2FA Setup](#user-registration-2fa-setup)
- [User Registration: 2FA Setup visited](#user-registration-2fa-setup-visited)
- [User Registration: phone setup visited](#user-registration-phone-setup-visited)
- [User Registration: personal key visited](#user-registration-personal-key-visited)
- [User Registration: piv cac disabled](#user-registration-piv-cac-disabled)
- [User Registration: piv cac enabled](#user-registration-piv-cac-enabled)
- [User Registration: piv cac setup visited](#user-registration-piv-cac-setup-visited)
- [WebAuthn Deleted](#webauthn-deleted)
- [WebAuthn Setup Visited](#webauthn-setup-visited)
- [WebAuthn Setup Submitted](#webauthn-setup-submitted)

<!-- /MarkdownTOC -->

### Definitions

- Doc Auth: Document authentication used for identity verification

- IdV: Identity Verification

- OTP: One-time password, used to send 2FA codes via SMS or Voice

- TOTP: Time-based One-Time Password, which is what authentication apps (such as
Google Authenticator) use.

- WebAuthn: refers to hardware security keys used for 2FA

### Account Reset
Tracks events related to a user requesting to delete their account during the
sign in process (because they have no other means to sign in).

#### When the request is first made
```ruby
event_properties: {
  event: 'request',
  sms_phone: true | false # does the user have phone as a 2FA option?
  totp: true | false, # does the user have an authentication app as a 2FA option?
  piv_cac: true | false, # does the user have PIV/CAC as a 2FA option?
  email_addresses: # number of email addresses the user has
}
```

Note: `sms_phone`, `totp`, and `piv_cac` above should all be replaced with:
```ruby
# analytics_attributes method in app/controllers/account_reset/request_controller.rb
mfa_method_counts: MfaContext.new(current_user).enabled_two_factor_configuration_counts_hash
```
This will return a hash that shows all of the user's 2FA configurations, such as:
```ruby
{:phone=>1, :auth_app=>1}
```

#### When the user clicks a link to cancel the request
Tracks when a user chooses to cancel the account deletion after clicking a link
in the email they received after making the initial request.
```ruby
event_properties: {
  event: 'visit', # this is fixed to 'cancel token validation' in PR 2665
  success: true | false, # whether or not the token was valid
  errors: # a hash of errors if any, otherwise an empty hash
}
```

#### When the user clicks the button to confirm the cancellation
```ruby
event_properties: {
  event: 'cancel',
  success: true | false, # whether or not the token was valid
  errors: # a hash of errors if any, otherwise an empty hash
}
```

#### When emails are sent to users who are eligible to delete their account.
When a user first requests to delete their account, they have to wait 24 hours,
and then they receive an email with a link that allows them to complete the
deletion. We have an AWS lambda that pings the `/api/account_reset/send_notifications`
endpoint every few minutes, and the IdP then checks to see which users are eligible,
then sends an email to them.

```ruby
event_properties: {
  event: 'notifications',
  count: # number of emails that were sent
}
```

#### When the user clicks the link in the email to complete the deletion
This displays a confirmation page where the user must click a button in order
to complete the deletion
```ruby
event_properties: {
  event: 'granted token validation',
  success: true | false, # whether or not the token was valid
  errors: # a hash of errors if any, otherwise an empty hash
}
```

#### When the user clicks the button to complete the deletion
```ruby
event_properties: {
  event: 'delete',
  account_age_in_days: # how long ago the user created their account,
  mfa_method_counts: # a hash of the 2FA configurations the user had,
  success: true | false, # whether or not the token was valid
  errors: # a hash of errors if any, otherwise an empty hash
}
```

### Account Deletion Requested
When the user deletes their account during one of these scenarios:
- during account creation
- from their account page after fully signing in
- others?

```ruby
event_properties: {
  request_came_from: # the referer that made the request, to see on which page the
                     # user made the request. If there is no referer, the value
                     # will be 'no referer'. Otherwise, it will show the Rails controller
                     # and action, such as 'users/sessions#new'
}
```

### Account deletion and reset visited
Tracks when a user visits the account deletion page during in the sign in flow.

### Doc Auth visited
Tracks when a user visits the Doc Auth page.

### Doc Auth submitted
```ruby
event_properties: {
  success: true | false,
  errors: # a hash of validation errors if any, otherwise an empty hash
  step: # the step the user was on.
        # Possible values: 'ssn', 'front_image', 'back_image', 'self_image'

}
```
Need Steve Urciuoli to confirm this, as well as possible error values.

### Email and Password Authentication
```ruby
event_properties: {
  success: true | false, # true if the user is signed in and not locked out
  user_locked_out: true | false,
  stored_location: session['user_return_to'],
  sp_request_url_present: true | false # tracks if the SP's request url is in the session
  remember_device: true | false, # is the remember device cookie present?
}
```

### Email Change Request
When the user changes their email from their account page. This only tracks
when they submit the form with the new email. In order for the email change
to take place, they must first confirm their new email address by clicking a
link in an email we send them. This is tracked in a separate event called
"Email Confirmation".
```ruby
event_properties: {
  success: true | false,
  errors: # a hash of validation errors if any, otherwise an empty hash
  email_already_exists: true | false, # true if the user tried to change their
                                      # email to an existing user's email
  email_changed: true | false # false if the user entered their current email
}
```

### Email Confirmation
```ruby
event_properties: {
  success: true | false,
  error: # a hash of validation errors if any, otherwise an empty hash
         # possible errors are: invalid token, empty token, token expired,
         # email was already confirmed
  existing_user: true | false # true if the user already confirmed their email
}
```
### Frontend: Browser capabilities

### IdV: basic info visited
No properties. This tracks a page view.

### IdV: basic info form submitted

### IdV: basic info vendor submitted

### IdV: cancellation visited

### IdV: cancellation confirmed

### IdV: come back later visited

### IdV: max attempts exceeded

### IdV: final resolution
Recorded once the user reaches the IdV confirmations page after successfully
verifying their identity

```ruby
 event_properties: {
   success: true,
   new_phone_added: true | false # true if the phone they used for IdV was not
                                 # the same as their 2FA phone, or if they did
                                 # not have a 2FA phone.
 }
```
See LG-832 for issues with the `new_phone_added` property. If they have been
resolved, please update this documentation.

### IdV: forgot password visited

### IdV: forgot password confirmed

### IdV: intro visited
No properties. This tracks a page view.

### IdV: jurisdiction visited

### IdV: jurisdiction form submitted

### IdV: phone confirmation form

### IdV: phone confirmation vendor

### Idv: Phone OTP attempts rate limited

### Idv: Phone OTP rate limited user

### Idv: Phone OTP sends rate limited

### IdV: phone confirmation otp resent

### IdV: phone confirmation otp sent

### IdV: phone confirmation otp submitted

### IdV: phone confirmation otp visited

### IdV: Phone OTP Delivery Selection Submitted

### IdV: Phone OTP delivery Selection Visited

### IdV: phone of record visited

### IdV: review complete

### IdV: review info visited
No properties. This tracks a page view.

### IdV: verification attempt cancelled

### Invalid Authenticity Token
This is triggered when an attempt is made to submit a form with an invalid CSRF
token.
```ruby
event_properties: {
  controller: # The controller where the user last tried to submit a form,
  user_signed_in: true | false
}
```

### Logout Initiated

### Multi-Factor Authentication
This event captures all the different ways someone authenticates via MFA.
This could be via SMS or Voice OTP, an Authenticator app (`totp`), entering the
personal key, PIV/CAC, or a hardware security key (`webauthn`). This is captured
in the `multi_factor_auth_method` property.

There are also different contexts for entering an MFA code, such as when
signing in, and when confirming a phone number. Confirming a phone number can
happen in 2 different contexts: when setting up the 2FA phone for the first time,
or when adding a new phone. These are captured in the `context` and
`confirmation_for_phone_change` properties.

```ruby
event_properties: {
  success: true | false,
  context: 'authentication' | 'confirmation',
  multi_factor_auth_method: 'sms' | 'voice' | 'totp' | 'personal key' | 'piv_cac' | 'webauthn',
  confirmation_for_phone_change: true | false
}
```

### Multi-Factor Authentication: enter OTP visited
No properties. This tracks a page view.

### Multi-Factor Authentication: enter personal key visited

### Multi-Factor Authentication: max attempts reached
This is triggered any time a user enters an MFA code incorrectly 3 times in a
row. This includes OTP, TOTP (authenticator app code), and recovery code.

### Multi-Factor Authentication: option list

### Multi-Factor Authentication: option list visited

### Multi-Factor Authentication: phone setup
When a user enters a new phone number. This is only to validate the phone number
format, not to confirm the phone.
```ruby
event_properties: {
  success: true | false,
  errors: # a hash of validation errors if any, otherwise an empty hash,
  otp_delivery_preference: 'sms' | 'voice'
}
```

### Multi-Factor Authentication: max otp sends reached

### OpenID Connect: bearer token authentication

### OpenID Connect: authorization request

### OpenID Connect: token

### OTP: Delivery Selection
Triggered when an OTP code is sent, which validates the `otp_delivery_preference`.
For example, if someone requests `voice` to a number that we can only send
an SMS to, we display an error message. This lets us know how often this event
contains failures.

```ruby
event_properties: {
  success: true | false,
  errors: # this should rarely contain an error since the only way to make this
          # fail is to pass in a delivery method other than 'sms' or 'voice' by
          # manipulating the form
  otp_delivery_preference: 'sms' | 'voice',
  resend: true | false # true if the user clicked the "resend" link,
  country_code: # the 2-letter country abbreviation,
  area_code: # the area code of the phone number,
  context: 'authentication' | 'confirmation'
}
```

### Password Changed
When a user changes their password. If the new password they entered is invalid,
an error will show up in this event.
```ruby
event_properties: {
  success: true | false,
  errors: # empty hash or any password validation errors
}
```

### Password Creation
When a user first creates their password during account creation.
```ruby
event_properties: {
  success: true | false,
  errors: # empty hash or any password validation errors
  request_id_present: true | false # tracks the presence of the `request_id` parameter
}
```

### Password Max Attempts Reached

### Password Reset: Email Submitted
This tracks the first step in the password reset process: entering the email
address.
```ruby
event_properties: {
  role: 'user' | 'tech' | 'admin',
  confirmed: true | false, # whether or not the user was already confirmed
  active_profile: true | false, # whether or not the user has an active profile,
                                # i.e. verified identity
  recaptcha_valid: true | false,
  recaptcha_present: true | false,
  recaptcha_enabled: true | false
}
```

### Password Reset: Password Submitted
This tracks the final step in the password reset process: entering the new
password.
```ruby
event_properties: {
  success: true | false,
  errors: # hash of password or password reset token validation errors, or empty hash
}
```

### Password Reset: Token Submitted
This tracks the second step in the password reset process: clicking the link
in the reset password email.
```ruby
event_properties: {
  success: true | false,
  errors: # hash of password reset token validation errors, or empty hash
}
```

### Password Reset: Email Form Visited

### Personal Key Viewed

### Phone Number Change: requested
No properties. This only tracks the fact that someone successfully submitted the
phone number change form with a new phone number. Whether or not this new phone
number was actually confirmed can be tracked via the
`Multi-Factor Authentication` event with `context: 'confirmation'` and
`confirmation_for_phone_change: true`.

### Phone Number Deletion: requested

### Profile Encryption: Invalid
This is mainly for debugging encryption issues. We should hopefully never see
this in production.
```ruby
event_properties: {
  error: # some profile encryption error, such as 'Unable to parse encrypted payload.'
}
```

### Profile: Created new personal key

### Rate Limit Triggered

### Response Timed Out

### SAML Auth
This tracks incoming LOA1 and LOA3 requests from a Service Provider
```ruby
event_properties: {
  authn_context: # the LOA, represented by a string such as 'http://idmanagement.gov/ns/assurance/loa/1',
  errors: # empty hash or one containing SAML request validation errors
  service_provider: # The SP, as defined on our `service_providers.yml`,
  success: true | false,
  finish_profile: true | false, # true if the user is still pending verification, such as if they
                                # requested to verify via USPS and haven't entered their code yet.
  idv: true | false, # true if LOA3 and the user has not already proofed.
                     # Note that this key won't be present if success is `false`
                     # because the SAML request must be valid before we can look
                     # up the user
}
```

### Session Timed Out
No event-specific properties. This is triggered when a user was signed in,
remained inactive for 15 minutes, and was auto signed out.

### Sign in page visited
No properties. This tracks a page view.

### TOTP Setup
When a user sets up an authentication app.
```ruby
event_properties: {
  success: true | false,
  errors: {},
  totp_secret_present: true | false # this was added to troubleshoot a bug where the TOTP secret
                                    # was no longer in the session
}
```

### TOTP Setup Visited

### TOTP: User Disabled TOTP
No event-specific properties.

### Twilio Phone Validation Failed

### Twilio SMS Inbound Message Received

### Twilio SMS Inbound Validation Failed

### User registration: agency handoff visited

### User registration: agency handoff complete

### User Registration: Email Submitted
The first step in the account creation process, when a user enters their email.
```ruby
event_properties: {
  success: true | false,
  errors: # empty hash or hash containing any email validation errors,
  email_already_exists: true | false,
  domain_name: # the domain name of the email entered by the user
  recaptcha_valid: true | false,
  recaptcha_present: true | false,
  recaptcha_enabled: true | false
}
```

### User Registration: Email Confirmation

### User Registration: Email Confirmation requested due to invalid token

### User Registration: enter email visited
No properties. This tracks a page view.

### User Registration: intro visited
No properties. This tracks a page view.

### User Registration: 2FA Setup

### User Registration: 2FA Setup visited

### User Registration: phone setup visited
No properties. This tracks a page view.

### User Registration: personal key visited

### User Registration: piv cac disabled

### User Registration: piv cac enabled

### User Registration: piv cac setup visited

### WebAuthn Deleted

### WebAuthn Setup Visited

### WebAuthn Setup Submitted
