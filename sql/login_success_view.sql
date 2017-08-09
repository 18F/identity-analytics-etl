CREATE VIEW password_success_rate
as (
      SELECT SUM(success::integer)/COUNT(*) as success_rate,
      date_trunc('hour', time) as hour
      FROM events
      WHERE otp_method = 'Email and Password Authentication'
      GROUP BY hour
    );

CREATE VIEW mfa_success_rate
as (
      SELECT SUM(success::integer)/COUNT(*) as success_rate,
      date_trunc('hour', time) as hour
      FROM events
      WHERE otp_method = 'Multi-Factor Authentication: max attempts reached'
      GROUP BY hour
    );
