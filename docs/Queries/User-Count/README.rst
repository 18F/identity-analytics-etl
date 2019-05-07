This directory provides queries for user count relative question.

User count metrics are usually for billing purpose, it has to be very accurate. It is why we use IDP DB instead of Redshift for this.

These two tables are important for user counts query, ``users`` and ``identities``.

Reference:

- Login.gov - Counting users: https://docs.google.com/document/d/1TvfyrsY2ncaHKtM9CVFYxhaUqDZ73xspGddh9R5DxeA/edit