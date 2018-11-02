.. _how-login-counts-users:

How Login.gov counts users
==============================================================================

How we count users, both our overall understanding of our real user population, and how we invoice agencies for public use of their specific applications.


Counting users as a whole
------------------------------------------------------------------------------

Numbers below are snapshots as of October 30-31, 2018. They were not all taken at the same, so the %’s are not perfectly precise.

**User counts, in stages of Login.gov use**:

1. Email entered: 10,489,327 (100%)
2. Email confirmed: 9,848,627 (93.8%, a 6.2% falloff from 1 to 2)
3. Completed MFA registration: ???
4. Signed into at least 1 SP: 9,489,715 (90.4%)
5. Signed into at least 2 SPs: 143,578 (1.3%)
    - At least 3: 14,676
    - At least 4: 577
    - At least 9: 1 (Vishal)

**Shown on Quicksite (“login-prod”) at the time**:

- ``Count of Users``: ~10,070,000 (10.07M)
    - Was determined to be a count of unique user IDs that showed up in our event logs. Essentially, was trying to measure stage 1 above (“Email entered”), but was incomplete for a few possible reasons.
- ``Fully Completed User Registrations``: 7,949,222
    - Not determined what this means.


Counting users for agency partners
------------------------------------------------------------------------------

We calculate the user population for an SP in 2 ways:

1. Users who created their Login.gov account (and completed registering MFA, tier #3 above) as a result of initiating their Login.gov session through that SP.
2. Users who have ever signed into this SP, regardless of how they created their Login.gov account and which SPs they have otherwise signed into.

**To bill an agency, we then**:

- Add all users from each SP associated with that agency agreement.
- Deduplicate these users across those SPs.
- Determine which users are “active” by [TBD].


Actions
------------------------------------------------------------------------------

**For users as a whole**:

- Calculate #3, “Completed MFA registration”.
- Replace our main “user count” number, on our dashboards and in our internal and external communication, with #3, “Completed MFA registration”.
- Make calculating #3, “Completed MFA registration”, quick and easy. It is currently very slow and difficult, which is not ideal since we want to use this as our primary user count.
- Figure out what “Fully Completed User Registrations” was intended to mean.

**For invoicing users**:

- Determine what our “active user” metric will be, which distinguishes which users are so inactive as to no longer be billable.
- Create an easy way to generate a report, per-agency and per-application, of the users of that application, according to the methodology described above.
