# IdP DB queries

This is a list of common queries we run for troubleshooting, tracking
data, and reporting data.

## Accessing the IdP Rails console
1. Clone the [identity-devops](https://github.com/18F/identity-devops) repo and
`cd` into it.

2. Run `AWS_PROFILE=login.gov bin/ssh-instance --newest asg-prod-idp`. I
recommend creating a shell alias for this. For example, you would add this to
your `.bash_profile`:
```console
alias prod='cd ~/projects/18f/identity-devops && export AWS_PROFILE=login.gov && bin/ssh-instance --newest asg-prod-idp'
```
Then you can SSH into prod by only typing `prod` at any time.

3. To run the Rails console:
```console
id-rails-console
```

## Troubleshooting

### Look up a user by email address

```ruby
user = User.find_with_email('moncef.belyamani@gsa.gov')
```

### Look up a user's events
```ruby
user.events.pluck(:event_type, :created_at)
```

### Look up the service providers the user has last signed into:
```ruby
user.identities.pluck(:service_provider, :last_authenticated_at)
```

### Is the user confirmed?
```ruby
user.confirmed?
```
This means they have confirmed their email address and created a password.

### Which 2FA methods has the user set up?
```ruby
MfaContext.new(user).enabled_two_factor_configuration_counts_hash
```
This will return something like:
```ruby
{:phone=>1, :auth_app=>1}
```
This means the user has both set up a phone and an authentication app as 2FA
methods.

## Metrics

### Counts

For most of these, you will need to temporarily increase the statement timeout:
```ruby
ActiveRecord::Base.connection.execute("SET statement_timeout = '60s'")
```

Each example below shows the ActiveRecord syntax you would use in the Rails
console, and the SQL equivalent below it. This is useful to have so that the
SQL can be copied and pasted when creating new queries in whatever internal tool
we end up building.

#### How many total users in the DB?
```ruby
User.count
```
```sql
SELECT COUNT(*) FROM "users";
```

#### How many confirmed users?
This means users who have both confirmed their email and created a password.
```ruby
User.select(:confirmed_at).where.not(confirmed_at: nil).count
```
```sql
SELECT COUNT("users"."confirmed_at")
FROM "users"
WHERE ("users"."confirmed_at" IS NOT NULL);
```

#### How many users have signed into at least 1 SP?
```ruby
User.joins(:identities).group('users.id').count.size
```
```sql
SELECT COUNT(*)
AS count_all, users.id AS users_id
FROM "users"
INNER JOIN "identities"
ON "identities"."user_id" = "users"."id"
GROUP BY users.id;
```

#### How many users have signed into at least 2 SPs?
```ruby
User.joins(:identities).group('users.id').having('count(user_id) > 1').count.size
```
```sql
SELECT COUNT(*)
AS count_all, users.id AS users_id
FROM "users"
INNER JOIN "identities"
ON "identities"."user_id" = "users"."id"
GROUP BY users.id
HAVING (count(user_id) > 1);
```

If this is something we will query frequently, we might consider adding a
counter cache to the Identities model:
```ruby
# app/models/identity.rb
belongs_to :user, counter_cache: true
```
We can then run:
```ruby
User.where('identities_count > ?', 1)
```

#### How many users have completed MFA setup?
We are adding a new column on the users table to make this faster to
query. See JIRA issue LG-802

#### How many users are there per SP?
```ruby
Identity.select(:service_provider).group('service_provider').count(:user_id)
```
```sql
SELECT COUNT("identities"."user_id")
AS count_user_id, "identities"."service_provider"
AS identities_service_provider
FROM "identities"
GROUP BY "identities"."service_provider";
```
