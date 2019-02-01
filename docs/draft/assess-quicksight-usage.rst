.. _access-quicksight-usage:

Assess QuickSight Usage
==============================================================================

.. contents::
    :local:

Relative Issue: https://github.com/18F/identity-analytics-etl/issues/171


What is QuickSight?
------------------------------------------------------------------------------

It is like a AWS powered Tableau, allow user to create data visualization dashboard with any data source.



How's QuickSight users account been created?
------------------------------------------------------------------------------

There are two ways of creating QuickSight account:

1. IAM Access: Use the ``18f-identity`` production AWS Account (QuickSight is in this account) IAM role if you have QuickSight access policy.
2. Email Access: Admin User with the AWS IAM access can create user account for others, it is an email / password only access.

Only a few people has the ``IAM Access``, mostly developers.

- Mossadeq Zia
- Andy Brody
- Justin Grevich
- Sanhe Hu

Most of users, especially external users are using ``Email Access``


QuickSight Access Monitor
------------------------------------------------------------------------------

- for ``IAM Access``: We can see login activity in the AWS IAM console
- for ``Email Access``: There's NO usage history.


QuickSight Users and Usage
------------------------------------------------------------------------------

- 21 GSA users
- 10 CBP users
- 8 Other users
- 39 total users

**Their email / contacts can be found at** https://docs.google.com/spreadsheets/d/1K_tl8QeEBo0POs9nUqsRGH6J9azy_QmtU0LXzYsEJ4Y/edit?usp=sharing

DaveJones (2019-01-28):
    @mossadeq and the DevOps team just did an “audit” of the quicksight user-base.  Most of the users are external to login.gov as part of sales and agency integrations

    over half the folks invited seem to have never created an account.
    
    

- In reaching out to our partners we received no responses. This may mean that this is not a frequently used tool, and thus may want to plan for depecration.
