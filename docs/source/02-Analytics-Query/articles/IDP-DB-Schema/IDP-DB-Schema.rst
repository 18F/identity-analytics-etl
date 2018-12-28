
account_reset_requests
----------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            cancelled_at
      - .. code-block:: sql
        
            account_reset_requests.cancelled_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            account_reset_requests.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            granted_at
      - .. code-block:: sql
        
            account_reset_requests.granted_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            granted_token
      - .. code-block:: sql
        
            account_reset_requests.granted_token
      - VARCHAR
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            account_reset_requests.id
      - BIGINT
    * - .. code-block:: sql
        
            reported_fraud_at
      - .. code-block:: sql
        
            account_reset_requests.reported_fraud_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            request_token
      - .. code-block:: sql
        
            account_reset_requests.request_token
      - VARCHAR
    * - .. code-block:: sql
        
            requested_at
      - .. code-block:: sql
        
            account_reset_requests.requested_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            account_reset_requests.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            account_reset_requests.user_id
      - INTEGER



agencies
--------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            agencies.id
      - BIGINT
    * - .. code-block:: sql
        
            name
      - .. code-block:: sql
        
            agencies.name
      - VARCHAR



agency_identities
-----------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            agency_id
      - .. code-block:: sql
        
            agency_identities.agency_id
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            agency_identities.id
      - BIGINT
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            agency_identities.user_id
      - INTEGER
    * - .. code-block:: sql
        
            uuid
      - .. code-block:: sql
        
            agency_identities.uuid
      - VARCHAR



ar_internal_metadata
--------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            ar_internal_metadata.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            key
      - .. code-block:: sql
        
            ar_internal_metadata.key
      - VARCHAR
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            ar_internal_metadata.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            value
      - .. code-block:: sql
        
            ar_internal_metadata.value
      - VARCHAR



authorizations
--------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            authorized_at
      - .. code-block:: sql
        
            authorizations.authorized_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            authorizations.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            authorizations.id
      - BIGINT
    * - .. code-block:: sql
        
            provider
      - .. code-block:: sql
        
            authorizations.provider
      - VARCHAR(255)
    * - .. code-block:: sql
        
            uid
      - .. code-block:: sql
        
            authorizations.uid
      - VARCHAR(255)
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            authorizations.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            authorizations.user_id
      - INTEGER



doc_auths
---------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            attempted_at
      - .. code-block:: sql
        
            doc_auths.attempted_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            attempts
      - .. code-block:: sql
        
            doc_auths.attempts
      - INTEGER
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            doc_auths.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            doc_auths.id
      - BIGINT
    * - .. code-block:: sql
        
            license_confirmed_at
      - .. code-block:: sql
        
            doc_auths.license_confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            selfie_confirmed_at
      - .. code-block:: sql
        
            doc_auths.selfie_confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            doc_auths.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            doc_auths.user_id
      - BIGINT



email_addresses
---------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            confirmation_sent_at
      - .. code-block:: sql
        
            email_addresses.confirmation_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            confirmation_token
      - .. code-block:: sql
        
            email_addresses.confirmation_token
      - VARCHAR(255)
    * - .. code-block:: sql
        
            confirmed_at
      - .. code-block:: sql
        
            email_addresses.confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            email_addresses.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            email_fingerprint
      - .. code-block:: sql
        
            email_addresses.email_fingerprint
      - VARCHAR
    * - .. code-block:: sql
        
            encrypted_email
      - .. code-block:: sql
        
            email_addresses.encrypted_email
      - VARCHAR
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            email_addresses.id
      - BIGINT
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            email_addresses.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            email_addresses.user_id
      - BIGINT



events
------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            events.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            event_type
      - .. code-block:: sql
        
            events.event_type
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            events.id
      - BIGINT
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            events.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            events.user_id
      - INTEGER



identities
----------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            access_token
      - .. code-block:: sql
        
            identities.access_token
      - VARCHAR
    * - .. code-block:: sql
        
            code_challenge
      - .. code-block:: sql
        
            identities.code_challenge
      - VARCHAR
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            identities.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            ial
      - .. code-block:: sql
        
            identities.ial
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            identities.id
      - BIGINT
    * - .. code-block:: sql
        
            last_authenticated_at
      - .. code-block:: sql
        
            identities.last_authenticated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            nonce
      - .. code-block:: sql
        
            identities.nonce
      - VARCHAR
    * - .. code-block:: sql
        
            rails_session_id
      - .. code-block:: sql
        
            identities.rails_session_id
      - VARCHAR
    * - .. code-block:: sql
        
            scope
      - .. code-block:: sql
        
            identities.scope
      - VARCHAR
    * - .. code-block:: sql
        
            service_provider
      - .. code-block:: sql
        
            identities.service_provider
      - VARCHAR(255)
    * - .. code-block:: sql
        
            session_uuid
      - .. code-block:: sql
        
            identities.session_uuid
      - VARCHAR(255)
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            identities.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            identities.user_id
      - INTEGER
    * - .. code-block:: sql
        
            uuid
      - .. code-block:: sql
        
            identities.uuid
      - VARCHAR
    * - .. code-block:: sql
        
            verified_attributes
      - .. code-block:: sql
        
            identities.verified_attributes
      - JSON



otp_requests_trackers
---------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            attribute_cost
      - .. code-block:: sql
        
            otp_requests_trackers.attribute_cost
      - VARCHAR
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            otp_requests_trackers.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            otp_requests_trackers.id
      - BIGINT
    * - .. code-block:: sql
        
            otp_last_sent_at
      - .. code-block:: sql
        
            otp_requests_trackers.otp_last_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            otp_send_count
      - .. code-block:: sql
        
            otp_requests_trackers.otp_send_count
      - INTEGER
    * - .. code-block:: sql
        
            phone_fingerprint
      - .. code-block:: sql
        
            otp_requests_trackers.phone_fingerprint
      - VARCHAR
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            otp_requests_trackers.updated_at
      - TIMESTAMP WITHOUT TIME ZONE



password_metrics
----------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            count
      - .. code-block:: sql
        
            password_metrics.count
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            password_metrics.id
      - BIGINT
    * - .. code-block:: sql
        
            metric
      - .. code-block:: sql
        
            password_metrics.metric
      - INTEGER
    * - .. code-block:: sql
        
            value
      - .. code-block:: sql
        
            password_metrics.value
      - DOUBLE PRECISION



phone_configurations
--------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            confirmation_sent_at
      - .. code-block:: sql
        
            phone_configurations.confirmation_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            confirmed_at
      - .. code-block:: sql
        
            phone_configurations.confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            phone_configurations.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            delivery_preference
      - .. code-block:: sql
        
            phone_configurations.delivery_preference
      - INTEGER
    * - .. code-block:: sql
        
            encrypted_phone
      - .. code-block:: sql
        
            phone_configurations.encrypted_phone
      - TEXT
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            phone_configurations.id
      - BIGINT
    * - .. code-block:: sql
        
            mfa_enabled
      - .. code-block:: sql
        
            phone_configurations.mfa_enabled
      - BOOLEAN
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            phone_configurations.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            phone_configurations.user_id
      - BIGINT



profiles
--------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            activated_at
      - .. code-block:: sql
        
            profiles.activated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            active
      - .. code-block:: sql
        
            profiles.active
      - BOOLEAN
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            profiles.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            deactivation_reason
      - .. code-block:: sql
        
            profiles.deactivation_reason
      - INTEGER
    * - .. code-block:: sql
        
            encrypted_pii
      - .. code-block:: sql
        
            profiles.encrypted_pii
      - TEXT
    * - .. code-block:: sql
        
            encrypted_pii_recovery
      - .. code-block:: sql
        
            profiles.encrypted_pii_recovery
      - TEXT
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            profiles.id
      - BIGINT
    * - .. code-block:: sql
        
            phone_confirmed
      - .. code-block:: sql
        
            profiles.phone_confirmed
      - BOOLEAN
    * - .. code-block:: sql
        
            ssn_signature
      - .. code-block:: sql
        
            profiles.ssn_signature
      - VARCHAR(64)
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            profiles.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            profiles.user_id
      - INTEGER
    * - .. code-block:: sql
        
            verified_at
      - .. code-block:: sql
        
            profiles.verified_at
      - TIMESTAMP WITHOUT TIME ZONE



remote_settings
---------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            contents
      - .. code-block:: sql
        
            remote_settings.contents
      - TEXT
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            remote_settings.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            remote_settings.id
      - BIGINT
    * - .. code-block:: sql
        
            name
      - .. code-block:: sql
        
            remote_settings.name
      - VARCHAR
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            remote_settings.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            url
      - .. code-block:: sql
        
            remote_settings.url
      - VARCHAR



schema_migrations
-----------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            version
      - .. code-block:: sql
        
            schema_migrations.version
      - VARCHAR



service_provider_requests
-------------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            service_provider_requests.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            service_provider_requests.id
      - BIGINT
    * - .. code-block:: sql
        
            issuer
      - .. code-block:: sql
        
            service_provider_requests.issuer
      - VARCHAR
    * - .. code-block:: sql
        
            loa
      - .. code-block:: sql
        
            service_provider_requests.loa
      - VARCHAR
    * - .. code-block:: sql
        
            requested_attributes
      - .. code-block:: sql
        
            service_provider_requests.requested_attributes
      - VARCHAR[]
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            service_provider_requests.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            url
      - .. code-block:: sql
        
            service_provider_requests.url
      - VARCHAR
    * - .. code-block:: sql
        
            uuid
      - .. code-block:: sql
        
            service_provider_requests.uuid
      - VARCHAR



service_providers
-----------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            aal
      - .. code-block:: sql
        
            service_providers.aal
      - INTEGER
    * - .. code-block:: sql
        
            acs_url
      - .. code-block:: sql
        
            service_providers.acs_url
      - TEXT
    * - .. code-block:: sql
        
            active
      - .. code-block:: sql
        
            service_providers.active
      - BOOLEAN
    * - .. code-block:: sql
        
            agency
      - .. code-block:: sql
        
            service_providers.agency
      - VARCHAR
    * - .. code-block:: sql
        
            agency_id
      - .. code-block:: sql
        
            service_providers.agency_id
      - INTEGER
    * - .. code-block:: sql
        
            approved
      - .. code-block:: sql
        
            service_providers.approved
      - BOOLEAN
    * - .. code-block:: sql
        
            assertion_consumer_logout_service_url
      - .. code-block:: sql
        
            service_providers.assertion_consumer_logout_service_url
      - TEXT
    * - .. code-block:: sql
        
            attribute_bundle
      - .. code-block:: sql
        
            service_providers.attribute_bundle
      - JSON
    * - .. code-block:: sql
        
            block_encryption
      - .. code-block:: sql
        
            service_providers.block_encryption
      - VARCHAR
    * - .. code-block:: sql
        
            cert
      - .. code-block:: sql
        
            service_providers.cert
      - TEXT
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            service_providers.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            description
      - .. code-block:: sql
        
            service_providers.description
      - TEXT
    * - .. code-block:: sql
        
            failure_to_proof_url
      - .. code-block:: sql
        
            service_providers.failure_to_proof_url
      - TEXT
    * - .. code-block:: sql
        
            fingerprint
      - .. code-block:: sql
        
            service_providers.fingerprint
      - VARCHAR
    * - .. code-block:: sql
        
            friendly_name
      - .. code-block:: sql
        
            service_providers.friendly_name
      - VARCHAR
    * - .. code-block:: sql
        
            ial
      - .. code-block:: sql
        
            service_providers.ial
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            service_providers.id
      - BIGINT
    * - .. code-block:: sql
        
            issuer
      - .. code-block:: sql
        
            service_providers.issuer
      - VARCHAR
    * - .. code-block:: sql
        
            logo
      - .. code-block:: sql
        
            service_providers.logo
      - TEXT
    * - .. code-block:: sql
        
            metadata_url
      - .. code-block:: sql
        
            service_providers.metadata_url
      - TEXT
    * - .. code-block:: sql
        
            native
      - .. code-block:: sql
        
            service_providers.native
      - BOOLEAN
    * - .. code-block:: sql
        
            piv_cac
      - .. code-block:: sql
        
            service_providers.piv_cac
      - BOOLEAN
    * - .. code-block:: sql
        
            piv_cac_scoped_by_email
      - .. code-block:: sql
        
            service_providers.piv_cac_scoped_by_email
      - BOOLEAN
    * - .. code-block:: sql
        
            redirect_uris
      - .. code-block:: sql
        
            service_providers.redirect_uris
      - VARCHAR[]
    * - .. code-block:: sql
        
            return_to_sp_url
      - .. code-block:: sql
        
            service_providers.return_to_sp_url
      - TEXT
    * - .. code-block:: sql
        
            signature
      - .. code-block:: sql
        
            service_providers.signature
      - VARCHAR
    * - .. code-block:: sql
        
            sp_initiated_login_url
      - .. code-block:: sql
        
            service_providers.sp_initiated_login_url
      - TEXT
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            service_providers.updated_at
      - TIMESTAMP WITHOUT TIME ZONE



users
-----

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            attribute_cost
      - .. code-block:: sql
        
            users.attribute_cost
      - VARCHAR
    * - .. code-block:: sql
        
            confirmation_sent_at
      - .. code-block:: sql
        
            users.confirmation_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            confirmation_token
      - .. code-block:: sql
        
            users.confirmation_token
      - VARCHAR(255)
    * - .. code-block:: sql
        
            confirmed_at
      - .. code-block:: sql
        
            users.confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            users.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            current_sign_in_at
      - .. code-block:: sql
        
            users.current_sign_in_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            current_sign_in_ip
      - .. code-block:: sql
        
            users.current_sign_in_ip
      - VARCHAR(255)
    * - .. code-block:: sql
        
            direct_otp
      - .. code-block:: sql
        
            users.direct_otp
      - VARCHAR
    * - .. code-block:: sql
        
            direct_otp_sent_at
      - .. code-block:: sql
        
            users.direct_otp_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            email_fingerprint
      - .. code-block:: sql
        
            users.email_fingerprint
      - VARCHAR
    * - .. code-block:: sql
        
            encrypted_email
      - .. code-block:: sql
        
            users.encrypted_email
      - TEXT
    * - .. code-block:: sql
        
            encrypted_otp_secret_key
      - .. code-block:: sql
        
            users.encrypted_otp_secret_key
      - TEXT
    * - .. code-block:: sql
        
            encrypted_password_digest
      - .. code-block:: sql
        
            users.encrypted_password_digest
      - VARCHAR
    * - .. code-block:: sql
        
            encrypted_phone
      - .. code-block:: sql
        
            users.encrypted_phone
      - TEXT
    * - .. code-block:: sql
        
            encrypted_recovery_code_digest
      - .. code-block:: sql
        
            users.encrypted_recovery_code_digest
      - VARCHAR
    * - .. code-block:: sql
        
            failed_attempts
      - .. code-block:: sql
        
            users.failed_attempts
      - INTEGER
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            users.id
      - BIGINT
    * - .. code-block:: sql
        
            idv_attempted_at
      - .. code-block:: sql
        
            users.idv_attempted_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            idv_attempts
      - .. code-block:: sql
        
            users.idv_attempts
      - INTEGER
    * - .. code-block:: sql
        
            last_sign_in_at
      - .. code-block:: sql
        
            users.last_sign_in_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            last_sign_in_ip
      - .. code-block:: sql
        
            users.last_sign_in_ip
      - VARCHAR(255)
    * - .. code-block:: sql
        
            locked_at
      - .. code-block:: sql
        
            users.locked_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            otp_delivery_preference
      - .. code-block:: sql
        
            users.otp_delivery_preference
      - INTEGER
    * - .. code-block:: sql
        
            phone_confirmed_at
      - .. code-block:: sql
        
            users.phone_confirmed_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            remember_created_at
      - .. code-block:: sql
        
            users.remember_created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            remember_device_revoked_at
      - .. code-block:: sql
        
            users.remember_device_revoked_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            reset_password_sent_at
      - .. code-block:: sql
        
            users.reset_password_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            reset_password_token
      - .. code-block:: sql
        
            users.reset_password_token
      - VARCHAR(255)
    * - .. code-block:: sql
        
            reset_requested_at
      - .. code-block:: sql
        
            users.reset_requested_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            role
      - .. code-block:: sql
        
            users.role
      - INTEGER
    * - .. code-block:: sql
        
            second_factor_attempts_count
      - .. code-block:: sql
        
            users.second_factor_attempts_count
      - INTEGER
    * - .. code-block:: sql
        
            second_factor_locked_at
      - .. code-block:: sql
        
            users.second_factor_locked_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            sign_in_count
      - .. code-block:: sql
        
            users.sign_in_count
      - INTEGER
    * - .. code-block:: sql
        
            totp_timestamp
      - .. code-block:: sql
        
            users.totp_timestamp
      - INTEGER
    * - .. code-block:: sql
        
            unconfirmed_email
      - .. code-block:: sql
        
            users.unconfirmed_email
      - VARCHAR(255)
    * - .. code-block:: sql
        
            unique_session_id
      - .. code-block:: sql
        
            users.unique_session_id
      - VARCHAR
    * - .. code-block:: sql
        
            unlock_token
      - .. code-block:: sql
        
            users.unlock_token
      - VARCHAR(255)
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            users.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            uuid
      - .. code-block:: sql
        
            users.uuid
      - VARCHAR(255)
    * - .. code-block:: sql
        
            x509_dn_uuid
      - .. code-block:: sql
        
            users.x509_dn_uuid
      - VARCHAR



usps_confirmation_codes
-----------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            code_sent_at
      - .. code-block:: sql
        
            usps_confirmation_codes.code_sent_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            usps_confirmation_codes.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            usps_confirmation_codes.id
      - BIGINT
    * - .. code-block:: sql
        
            otp_fingerprint
      - .. code-block:: sql
        
            usps_confirmation_codes.otp_fingerprint
      - VARCHAR
    * - .. code-block:: sql
        
            profile_id
      - .. code-block:: sql
        
            usps_confirmation_codes.profile_id
      - INTEGER
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            usps_confirmation_codes.updated_at
      - TIMESTAMP WITHOUT TIME ZONE



usps_confirmations
------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            usps_confirmations.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            entry
      - .. code-block:: sql
        
            usps_confirmations.entry
      - TEXT
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            usps_confirmations.id
      - BIGINT
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            usps_confirmations.updated_at
      - TIMESTAMP WITHOUT TIME ZONE



webauthn_configurations
-----------------------

.. list-table:: columns
    :class: sortable
    :header-rows: 1
    :stub-columns: 0

    * - name
      - fullname
      - type
    * - .. code-block:: sql
        
            created_at
      - .. code-block:: sql
        
            webauthn_configurations.created_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            credential_id
      - .. code-block:: sql
        
            webauthn_configurations.credential_id
      - TEXT
    * - .. code-block:: sql
        
            credential_public_key
      - .. code-block:: sql
        
            webauthn_configurations.credential_public_key
      - TEXT
    * - .. code-block:: sql
        
            id
      - .. code-block:: sql
        
            webauthn_configurations.id
      - BIGINT
    * - .. code-block:: sql
        
            name
      - .. code-block:: sql
        
            webauthn_configurations.name
      - VARCHAR
    * - .. code-block:: sql
        
            updated_at
      - .. code-block:: sql
        
            webauthn_configurations.updated_at
      - TIMESTAMP WITHOUT TIME ZONE
    * - .. code-block:: sql
        
            user_id
      - .. code-block:: sql
        
            webauthn_configurations.user_id
      - BIGINT
