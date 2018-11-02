Analytics How To
==============================================================================


Connect GSA VPN
------------------------------------------------------------------------------

Reference: https://handbook.18f.gov/anyconnect/

1. Launch Cisco Anyconnect.
2. Enter: vpn.gsa.gov/adcontractors
3. Enter your GSA Enterprise Account and Password. GSA Enterprise Account usually is your {firstname}{lastname} with no space, lowercase; password is your GSA email password.
4. Go https://secureauth.gsa.gov/secureauth14/, get one time password.



 Ask the new team member to extract PIV public key following these steps: https://github.com/18F/identity-private/wiki/Operations:-MacOSX-PIV-to-SSH-key-extraction and create a file under https://github.com/18F/identity-devops-private/tree/master/chef/data_bags/users that has the PIV key in it and all the environments they need access to.


Connect Redshift
------------------------------------------------------------------------------

There are two Redshift, **prod Redshift** and **staging Redshift**. Both two redshift cluster are under ``18f-identity-analytics`` account. You have to login to **Jumphost** EC2 machine, then use ``psql`` to connect to the Redshift. There are also two Jumphost, **prod Jumphost** and **staging Jumphost**.

There are two ways to login to Jumphost:

1. Use ssh + AWS Credential:

    - staging: ``export AWS_PROFILE=login.gov && bin/ssh-instance asg-staging-jumphost``

2. Use ssh + PIV Card:

    - staging: ``ssh -2 -I /usr/local/lib/opensc-pkcs11.so sanhehu@jumphost.staging.login.gov``
    - prod: ``ssh -2 -I /usr/local/lib/opensc-pkcs11.so sanhehu@jumphost.prod.login.gov``
    - prod: ``ssh -2 -I /usr/local/lib/opensc-pkcs11.so sanhehu@34.216.215.113``

When you are in **Jumphost**:

- Connect to Redshift ``psql`` shell: ``psql -h tf-prod-redshift-cluster.cgdzf4brs0dt.us-west-2.redshift.amazonaws.com -U sanhehu -d analytics -p 5439``
- You can alter your password in ``psql``: ``ALTER USER sanhehu password 'your_new_password';``


**Copy file from Jumphost to local**: at your local machine, run ``scp -o PKCS11Provider=/usr/local/lib/opensc-pkcs11.so {username}@34.216.215.113:{remote_path} {local_path}``


**Get public IP address of EC2**: ``curl https://checkip.amazonaws.com``