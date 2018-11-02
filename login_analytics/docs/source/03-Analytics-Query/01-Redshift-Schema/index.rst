.. contents::

.. _prod.redshift.schema.database:

Redshift Database Schema
==============================================================================

**List of Tables**::

     schema |          name           | type  |  owner
    --------+-------------------------+-------+---------
     public | events                  | table | awsuser
     public | events_devices          | table | awsuser
     public | events_email            | table | awsuser
     public | events_phone            | table | awsuser
     public | pageviews               | table | awsuser
     public | service_providers       | table | awsuser
     public | uploaded_files          | table | awsuser
     public | uploaded_files_20180620 | table | awsuser
     public | user_agents             | table | awsuser


Number of Rows (updated at 2018-10-24):

.. code-block:: SQL

    SELECT COUNT(*) FROM {table_name};

- events: 863,295,925
- events_email: 9,429,371
- events_phone: 29,276,932
- events_devices: 781,655,803
- events_pageviews: 1,118,548,826
- service_providers: 26
- uploaded_files: 2,404,992
- user_agents: 0


**List of Views**::

     schema |               name               | type |  owner
    --------+----------------------------------+------+---------
     public | account_reset_and_cancel         | view | awsuser
     public | avg_daily_signups_by_month       | view | awsuser
     public | daily_active_users               | view | awsuser
     public | email_domain_return_rate         | view | awsuser
     public | experience_durations             | view | awsuser
     public | experience_durations_visitor_id  | view | awsuser
     public | hourly_active_users              | view | awsuser
     public | mfa_success_rate                 | view | awsuser
     public | monthly_active_users             | view | awsuser
     public | monthly_active_users_by_sp       | view | awsuser
     public | monthly_signups                  | view | awsuser
     public | monthly_signups_with_user_logins | view | awsuser
     public | password_success_rate            | view | awsuser
     public | password_success_rate_by_month   | view | awsuser
     public | personal_key_success_rate        | view | awsuser
     public | return_rate                      | view | awsuser

.. note::

    **View** is a virtual table generated from a SQL query.

    Reference: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_VIEW.html


.. _prod.redshift.schema.table:

Table Schema
------------------------------------------------------------------------------


.. _prod.redshift.schema.table.events:

table.events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`.

Schema::

          Column      |            Type             | Modifiers
    ------------------+-----------------------------+-----------
     id               | character varying(40)       | not null
     name             | character varying(255)      | not null
     user_agent       | character varying(4096)     |
     user_id          | character varying(40)       |
     user_ip          | character varying(50)       |
     host             | character varying(255)      |
     visit_id         | character varying(40)       |
     visitor_id       | character varying(40)       |
     time             | timestamp without time zone |
     event_properties | character varying(4096)     |
     success          | boolean                     |
     existing_user    | boolean                     |
     otp_method       | character varying(20)       |
     context          | character varying(20)       |
     method           | character varying(20)       |
     authn_context    | character varying(50)       |
     service_provider | character varying(255)      |
     loa3             | boolean                     |
     active_profile   | boolean                     |
     errors           | character varying(4096)     |

:ref:`Column Description <prod.redshift.schema.column.events>`.

Sample Data::

                      id                  |                      name                      |                                                                user_agent                                                                |               user_id                |    user_ip     |       host       |               visit_id               |              visitor_id              |        time         |                                                                     event_properties                                                                     | success | existing_user | otp_method |    context     | method | authn_context |                      service_provider                      | loa3 | active_profile | errors
    --------------------------------------+------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+----------------+------------------+--------------------------------------+--------------------------------------+---------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------+---------+---------------+------------+----------------+--------+---------------+------------------------------------------------------------+------+----------------+--------
     80fc5f87-3530-4f50-b797-2aa1748f8d07 | OTP: Delivery Selection                        | Mozilla/5.0 (X11; CrOS x86_64 10718.88.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.118 Safari/537.36                      | 7a2a1766-6737-4a06-813e-5f584a525535 | 65.222.189.201 | secure.login.gov | 3fdb5a9e-851e-4577-932f-e9726a6dde4b | b49dff5d-bda8-4892-a4ad-03d3db0a85e0 | 2018-10-12 00:00:00 | {"success": true, "errors": {}, "otp_delivery_preference": "sms", "resend": null, "country_code": "US", "area_code": "210", "context": "authentication"} | t       |               |            | authentication |        |               | urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD |      |                | {}
     eac233c7-ec06-41e7-b831-c0e25be6751b | Sign in page visited                           | Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; rv:11.0) like Gecko                                                               | anonymous-uuid                       | 71.244.247.225 | secure.login.gov | e78ce2af-199b-4591-b286-9df860836abe | 3e20450b-e835-46c2-8ccf-aa5369b0ec93 | 2018-10-12 00:00:02 | {"flash": null, "stored_location": null}                                                                                                                 |         |               |            |                |        |               | urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD |      |                | null
     59c93af2-6e39-4480-af9a-24519327051e | Email and Password Authentication              | Mozilla/5.0 (Linux; Android 7.0; SM-N920T Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36 | 30109861-cfa2-461a-aa7d-a4d2402fab67 | 73.152.228.112 | secure.login.gov | c2c040e6-8a0d-4426-9903-1df8ef117576 | 4aedf034-9e7f-446d-8cef-948d2b313818 | 2018-10-12 00:00:03 | {"success": true, "user_locked_out": false, "stored_location": null, "sp_request_url_present": true}                                                     | t       |               |            |                |        |               | urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD |      |                | null
     de10f93c-fa8e-494f-bbaa-026632b478c4 | Email and Password Authentication              | Mozilla/5.0 (Linux; Android 5.1; 9010X Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36           | 5e6df9d5-e2fc-47a4-ba20-42cc1b05e862 | 105.105.4.133  | secure.login.gov | a5a74fd9-232a-4ca1-99d0-5403ea8438f4 | 8b9e698f-aebf-4d78-872a-74e5e7d1a3fb | 2018-10-12 00:00:03 | {"success": true, "user_locked_out": false, "stored_location": null, "sp_request_url_present": true}                                                     | t       |               |            |                |        |               | urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD |      |                | null
     76972936-8f97-46a1-a432-3cf2217ff541 | Multi-Factor Authentication: enter OTP visited | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36                      | d564f17a-0c9f-43b7-8709-2f519cdb7623 | 162.72.84.185  | secure.login.gov | 53b04792-20eb-4e6d-a2e8-cbd353cdd79b | 245f878d-51d4-4923-b9c2-dfc851f182b0 | 2018-10-12 00:00:04 | {"context": "authentication", "multi_factor_auth_method": "sms", "confirmation_for_phone_change": false}                                                 |         |               |            | authentication |        |               | urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD |      |                | null


.. _prod.redshift.schema.table.events_email:

table.events_email
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`.

Schema::

       Column    |            Type             | Modifiers
    -------------+-----------------------------+-----------
     id          | character varying(40)       | not null
     name        | character varying(255)      | not null
     domain_name | character varying(255)      |
     time        | timestamp without time zone |

Sample Data::

                      id                  |                name                |  domain_name   |        time
    --------------------------------------+------------------------------------+----------------+---------------------
     247f425c-8b74-44df-9322-54f49712f7bb | User Registration: Email Submitted | coparenter.org | 2018-10-12 00:00:16
     70413517-df03-43eb-83e1-b5ce0435aa61 | User Registration: Email Submitted | gmail.com      | 2018-10-12 00:01:02
     b13c3897-73f6-460e-86f3-ba2e5f3cbb8f | User Registration: Email Submitted | gmail.com      | 2018-10-12 00:01:32
     b9dc978a-a335-4c42-9f5c-88db0f3b8f27 | User Registration: Email Submitted | icloud.com     | 2018-10-12 00:03:07
     44970f6b-0da5-4009-9211-051b6aaf1809 | User Registration: Email Submitted | gmail.com      | 2018-10-12 00:03:37


.. _prod.redshift.schema.table.events_phone:

table.events_phone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`.

Schema::

        Column    |            Type             | Modifiers
    --------------+-----------------------------+-----------
     id           | character varying(40)       | not null
     visit_id     | character varying(40)       |
     visitor_id   | character varying(40)       |
     area_code    | character varying(10)       | not null
     country_code | character varying(10)       | not null
     time         | timestamp without time zone |

Sample Data::

                      id                  |               visit_id               |              visitor_id              | area_code | country_code |        time
    --------------------------------------+--------------------------------------+--------------------------------------+-----------+--------------+---------------------
     59fb150f-b56b-4323-8c7e-b274a8e04848 | f6b8afaa-2b27-47e2-9ad5-5139fbdf7be4 | b936d3f3-b3cf-4b99-9f70-15b9468ca6c0 | 339       | US           | 2018-10-12 00:00:06
     8679413a-e56b-4d2e-8ed9-e5b715a7f2d3 | 41aef6f4-ab76-4808-aa36-73039f377e71 | b84ff647-0d5c-4034-bc83-448f56d47cb5 | 818       | US           | 2018-10-12 00:00:27
     8d78ef66-056b-4984-ba5c-df2c088a1388 | dd92fab3-08b0-4e63-9246-204bcee9f5e8 | 29ec82d5-0ea2-4832-a06e-68f5f6e23a7e | 618       | US           | 2018-10-12 00:01:15
     780b46b5-98e9-4819-808b-761d8381400b | 2b7b043c-250c-471e-95e6-b3319dc1ce32 | 51d81dc3-f692-493c-9c7f-77de58567930 | 580       | US           | 2018-10-12 00:01:20
     e3e96194-4146-458a-9a53-7eb4ba9818eb | 2962d760-f7c0-4774-bc49-00753d7428a9 | 542d142c-73a8-48d3-982e-9fc8f202d65b | 416       | CA           | 2018-10-12 00:01:38


.. _prod.redshift.schema.table.events_devices:

table.events_devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`.

Schema::

              Column          |            Type             | Modifiers
    --------------------------+-----------------------------+-----------
     id                       | character varying(40)       | not null
     name                     | character varying(255)      | not null
     user_agent               | character varying(4096)     |
     browser_name             | character varying(255)      |
     browser_version          | character varying(255)      |
     browser_platform_name    | character varying(255)      |
     browser_platform_version | character varying(255)      |
     browser_device_name      | character varying(255)      |
     browser_device_type      | character varying(255)      |
     browser_bot              | boolean                     |
     time                     | timestamp without time zone |


Sample Data::

                      id                  |                 name                  |                                                                   user_agent                                                                   |   browser_name    | browser_version | browser_platform_name | browser_platform_version | browser_device_name | browser_device_type | browser_bot |        time
    --------------------------------------+---------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+-------------------+-----------------+-----------------------+--------------------------+---------------------+---------------------+-------------+---------------------
     657f3033-ebaa-4609-8af6-2d062aa22907 | OTP: Delivery Selection               | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134              | Microsoft Edge    | 17.17134        | Windows               | 10                       |                     | desktop             | f           | 2018-10-12 00:00:00
     0bf3f68a-68c8-468b-924a-09b01a95cdc7 | Sign in page visited                  | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36                            | Chrome            | 69.0.3497.100   | Windows               | 10                       |                     | desktop             | f           | 2018-10-12 00:00:01
     227c5b3b-8d3e-415a-9f8f-31ab59c65cd6 | Email and Password Authentication     | Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36                             | Chrome            | 69.0.3497.100   | Windows               | 8.1                      |                     | desktop             | f           | 2018-10-12 00:00:05
     7fb448e3-caf2-4d2e-8bd3-21d899c1bbcd | OpenID Connect: authorization request | Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1 | Chrome Mobile iOS | 69.0.3497.105   | iOS                   | 12.0                     | iPhone              | smartphone          | f           | 2018-10-12 00:00:05
     96b7682c-7b6c-43ee-ada9-b915bb260e12 | Password Reset: Token Submitted       | Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1      | Mobile Safari     | 11.0            | iOS                   | 11.4.1                   | iPhone              | smartphone          | f           | 2018-10-12 00:00:06


.. _prod.redshift.schema.table.pageviews:

table.pageviews
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`. It stores HTTP requests history.

Schema::

       Column   |            Type             | Modifiers
    ------------+-----------------------------+-----------
     method     | character varying(10)       | not null
     path       | character varying(1024)     |
     format     | character varying(255)      |
     controller | character varying(100)      |
     action     | character varying(30)       |
     status     | smallint                    |
     duration   | double precision            |
     user_id    | character varying(80)       |
     user_agent | character varying(4096)     |
     ip         | character varying(80)       |
     host       | character varying(255)      |
     timestamp  | timestamp without time zone |
     uuid       | character varying(80)       | not null

Sample Data::

     method |               path                | format |                controller                | action | status | duration |               user_id                |                                                                user_agent                                                                 |       ip       |       host       |      timestamp      |                 uuid
    --------+-----------------------------------+--------+------------------------------------------+--------+--------+----------+--------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------+----------------+------------------+---------------------+--------------------------------------
     GET    | /api/openid_connect/certs         | html   | OpenidConnect::CertsController           | index  |    200 |     1.85 | anonymous-uuid                       | Apache-HttpClient/4.5.3 (Java/1.7.0_141)                                                                                                  | 66.77.18.211   | secure.login.gov | 2018-10-12 00:00:00 | f566e7be-5f92-4556-894b-326b37660c06
     GET    | /users/two_factor_authentication  | html   | Users::TwoFactorAuthenticationController | show   |    302 |   175.81 | 38ee4578-47df-4c2f-9f62-50bc26ce8d6c | Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.0 Mobile/15E148 Safari/604.1 | 107.77.213.126 | secure.login.gov | 2018-10-12 00:00:00 | 6b09e04f-6d1e-4119-b20a-5b93c94e61bf
     GET    | /users/password/edit?timeout=true | html   | Users::ResetPasswordsController          | edit   |    302 |    15.95 | anonymous-uuid                       | Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko                                                                             | 74.217.90.250  | secure.login.gov | 2018-10-12 00:00:01 | 0a36ba58-8e32-4641-b587-41c465cbcdb3
     GET    | /users/password/edit              | html   | Users::ResetPasswordsController          | edit   |    200 |    44.87 | anonymous-uuid                       | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36                       | 40.107.226.57  | secure.login.gov | 2018-10-12 00:00:01 | b21408b1-878d-4aa9-8cfb-3a0c3b92179b
     GET    | /users/two_factor_authentication  | html   | Users::TwoFactorAuthenticationController | show   |    302 |   220.41 | badc1cbb-150c-4dd8-890b-d678c16f13f1 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36                       | 173.76.109.209 | secure.login.gov | 2018-10-12 00:00:03 | 65462715-aa12-423f-9e06-1a9d4021335d

.. note::

    Updated on 2018-10-19

    Currently this table are not used in any of existing analytic query.


.. _prod.redshift.schema.table.service_providers:

table.service_providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`dimension-table`.

Schema::

          Column      |          Type          | Modifiers
    ------------------+------------------------+-----------
     events_sp        | character varying(255) |
     service_provider | character varying(255) |

Sample Data::

                                 events_sp                              |          service_provider
    --------------------------------------------------------------------+------------------------------------
     urn:gov:gsa:openidconnect.profiles:sp:sso:VGITeam:NOME             | gsa-VGI
     urn:gov:dhs.cbp.jobs:openidconnect:aws-cbp-ttp                     | ttp
     urn:gov:dot:openidconnect.profiles:sp:sso:dot:nr_auth              | dot
     urn:gov:gsa:open-id-connect:sp:sso:usda-forestservice:epermit-prod | Forest Service Open Forest Permits
     urn:gov:gsa:openidconnect.profiles:sp:sso:nga:mage                 | nga


.. _prod.redshift.schema.table.uploaded_files:

table.uploaded_files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`fact-table`.

::

       Column    |            Type             | Modifiers
    -------------+-----------------------------+-----------
     s3filename  | character varying(500)      | not null
     destination | character varying(255)      | not null
     uploaded_at | timestamp without time zone |


.. _prod.redshift.schema.table.user_agents:

table.user_agents
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a :ref:`dimension-table`.

Schema::

       Column   |          Type          | Modifiers
    ------------+------------------------+-----------
     user_agent | character varying(255) | not null
     browser    | character varying(100) |
     platform   | character varying(100) |
     version    | character varying(100) |


Column Description
------------------------------------------------------------------------------


.. _prod.redshift.schema.column.events:

table.events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Table Schema: :ref:`prod.redshift.table.events`


.. _prod.redshift.schema.column.events.name:

table.events.name
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: SQL

    SELECT DISTINCT(name) FROM events ORDER BY name;

::

                                     name
    ----------------------------------------------------------------------
     Account Deletion Requested
     Account Page Visited
     Account Reset
     Account deletion and reset visited
     Email Change Request
     Email Confirmation
     Email Confirmation requested due to invalid token
     Email and Password Authentication
     IdV: Phone OTP Delivery Selection Submitted
     IdV: Phone OTP delivery Selection Visited
     IdV: basic info form submitted
     IdV: basic info vendor submitted
     IdV: basic info visited
     IdV: cancellation confirmed
     IdV: cancellation visited
     IdV: final resolution
     IdV: intro visited
     IdV: jurisdiction form submitted
     IdV: jurisdiction visited
     IdV: phone confirmation form
     IdV: phone confirmation otp sent
     IdV: phone confirmation otp submitted
     IdV: phone confirmation otp visited
     IdV: phone confirmation vendor
     IdV: phone of record visited
     IdV: review complete
     IdV: review info visited
     Invalid Authenticity Token
     Logout Initiated
     Multi-Factor Authentication
     Multi-Factor Authentication: enter OTP visited
     Multi-Factor Authentication: enter personal key visited (Personal Key)
     Multi-Factor Authentication: max attempts reached
     Multi-Factor Authentication: max otp sends reached
     Multi-Factor Authentication: option list
     Multi-Factor Authentication: option list visited
     Multi-Factor Authentication: phone setup
     OTP: Delivery Selection
     OpenID Connect: authorization request
     OpenID Connect: bearer token authentication
     OpenID Connect: logout
     OpenID Connect: token
     Password Changed
     Password Creation
     Password Max Attempts Reached
     Password Reset: Email Form Visited
     Password Reset: Email Submitted
     Password Reset: Password Submitted
     Password Reset: Token Submitted
     Personal Key Viewed
     Phone Number Change: requested
     Profile: Created new personal key
     Rate Limit Triggered
     Response Timed Out
     SAML Auth
     Session Timed Out
     Sign in page visited
     TOTP Setup
     TOTP Setup Visited
     TOTP: User Disabled TOTP
     Twilio Phone Validation Failed
     User Registration: 2FA Setup
     User Registration: 2FA Setup visited
     User Registration: Email Confirmation
     User Registration: Email Confirmation requested due to invalid token
     User Registration: Email Submitted
     User Registration: enter email visited
     User Registration: intro visited
     User Registration: personal key visited
     User Registration: phone setup visited
     User Registration: piv cac disabled
     User Registration: piv cac enabled
     User Registration: piv cac setup visited
     User registration: agency handoff complete
     User registration: agency handoff visited
     WebAuthn Deleted
     WebAuthn Setup Submitted
     WebAuthn Setup Visited


**Sign Up Related Events**:

``events name`` realted to ``Enter the Email``:

- `User Registration: Email Submitted`

``events name`` realted to ``Confirm their Email``:

- ``User Registration: Email Confirmation``

``events name`` realted to ``Set a strong password``:

- ``Password Creation``:

``events name`` realted to ``Set up MFA``:

- ``events.name = 'Multi-Factor Authentication' AND context = 'confirmation' AND event_properties.confirmation_for_phone_change IS FALSE``
- ``TOTP Setup``
- ``WebAuthn Setup Submitted``
- ``User Registration: piv cac enabled``


**Sign In Related Events**:

- ``Email and Password Authentication``

**Personal Key Access Related Events**:

- ``User Registration: personal key visited``
- ``Personal Key Viewed``
- ``Profile: Created new personal key``: users go to their profile and clicks the ``Generate a new personal key`` button.
- ``Multi-Factor Authentication: enter personal key visited``


.. _prod.redshift.schema.column.events.service_provider:

table.events.service_provider
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Its a foreign key of ``table.service_providers.events_sp``.

See :ref:`prod.redshift.schema.column.service_providers` for more info.

.. code-block:: SQL

    SELECT DISTINCT(service_provider) FROM events ORDER BY service_provider;


.. _prod.redshift.schema.column.events.context:

table.events.context
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. code-block:: SQL

    SELECT DISTINCT(context) FROM events ORDER BY context;

Example::

         context
    ------------------
     ''
     authentication
     confirmation
     idv
     reauthentication


.. _prod.redshift.schema.column.service_providers:

table.service_providers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Table Schema: :ref:`prod.redshift.table.service_providers`

Column Description:

- ``events_sp``: the unique identifier for service provider in :ref:`events.service_provider <prod.redshift.schema.table.events>` column.
- ``service_provider``: Human readable service provider name.

::

                                  events_sp                              |                  service_provider
     --------------------------------------------------------------------+----------------------------------------------------
      urn:gov:gsa:openidconnect.profiles:sp:sso:doe:fergas               | Import/Export Authorization Portal for Natural Gas
      urn:gov:gsa:openidconnect.profiles:sp:sso:VGITeam:NOME             | gsa-VGI
      urn:gov:gsa:openidconnect.profiles:sp:sso:OPM:USAJOBS:PROD         | opm-usajobs
      urn:gov:gsa:SAML:2.0.profiles:sp:sso:usss:pix                      | secret_service
      urn:gov:gsa:openidconnect.profiles:sp:sso:dot:login                | dot
      urn:gov:gsa:openidconnect.profiles:sp:sso:nga:hiper_look           | nga
      urn:gov:gsa:openidconnect.profiles:sp:sso:nga:mage                 | nga
      urn:gov:dot:openidconnect.profiles:sp:sso:dot:nr_auth              | dot
      urn:gov:dhs.cbp.jobs:openidconnect:cert:app                        | cbp-jobs
      urn:gov:gsa:SAML:2.0.profiles:sp:sso:rails-int                     | gsa
      urn:gov:dhs.cbp.pspd.oars:openidconnect:prod:app                   | oars
      urn:gov:gsa:openidconnect.profiles:sp:sso:gsa:sam_uat              | sam_uat
      urn:gov:gsa:openidconnect.profiles:sp:sso:dod:officemovemilprod    | move.mil
      urn:gov:gsa:SAML:2.0.profiles:sp:sso:RRB:BOS-Pre-Prod              | rrb
      urn:gov:dhs.cbp.jobs:openidconnect:jenkins-pspd-credential-service | cbp-jobs
      urn:gov:gsa:open-id-connect:sp:sso:usda-forestservice:epermit-prod | Forest Service Open Forest Permits
      urn:gov:dhs.cbp.jobs:openidconnect:prod                            | cbp-jobs
      urn:gov:dhs.cbp.jobs:openidconnect:aws-cbp-ttp                     | ttp
      urn:gov:gsa:openidconnect.profiles:sp:sso:RRB:BOS_AA1_Prod         | Railroad Retirement Board
      https://chat.usds.gov/saml/metadata                                | USDS-hipchat
      urn:gov:gsa:openidconnect.profiles:sp:sso:gsa:sam                  | sam_prod
      urn:gov:gsa:openidconnect.profiles:sp:sso:nga:landingpage          | nga
      urn:gov:gsa:openidconnect.profiles:sp:sso:dod:mymovemilprod        | move.mil
      urn:gov:gsa:openidconnect.profiles:sp:sso:dod:tspmovemilprod       | tsp.move.mil
      urn:gov:dhs.cbp.opa.mycbp:openidconnect:prod                       | MyCBP
      urn:gov:dhs.cbp.jobs:openidconnect:prod:app                        | cbp-jobs
