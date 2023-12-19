# Okta-user-cli-tool
(De)activates/Deletes users from Okta including their group membership

This tool is intended to be used as a CLI tool to (de)activate/delete users from Okta including their group membership.

Examples:

Deactivate the 2 given users
```
python disable_users.py --api-token <Okta API token> --domain company.okta.com --userids 00u1ugrngdstLcUvb0h8 00u1ugrmhyqeNJXz40h8 --action deactivate
```
Activate the 2 given users
```
python disable_users.py --api-token <Okta API token> --domain company.okta.com --userids 00u1ugrngdstLcUvb0h8 00u1ugrmhyqeNJXz40h8 --action activate
```
Delete the 2 given users (These users need to be de-activated first, deletion of an active user will equal deactivation of that user)
```
python disable_users.py --api-token <Okta API token> --domain company.okta.com --userids 00u1ugrngdstLcUvb0h8 00u1ugrmhyqeNJXz40h8 --action delete
```
Delete the 2 given users, but remove their existing group membership first
```
python disable_users.py --api-token <Okta API token> --remove-group-membership  --domain company.okta.com --userids 00u1ugrngdstLcUvb0h8 00u1ugrmhyqeNJXz40h8 --action delete
```
