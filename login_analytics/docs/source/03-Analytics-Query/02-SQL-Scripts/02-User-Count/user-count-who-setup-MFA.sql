SELECT
    COUNT(DISTINCT events.user_id)
FROM events
WHERE
    (
        events.name = 'User Registration: piv cac enabled'
        AND events.context = 'confirmation'
    ) OR
    (
        events.name IN (
            'TOTP Setup',
            'WebAuthn Setup Submitted',
            'User Registration: piv cac enabled'
        )
    )
    AND events.success IS TRUE;