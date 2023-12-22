import requests
import argparse

def clean_url(url):
    if url.startswith('https://'):
        url = url[8:]
    if url.endswith('/'):
        url = url[:-1]
    return url

def fetch_groups(user_id):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'SSWS ' + OKTA_KEY}
    url = 'https://' + domain + '/api/v1/users/' + user_id + '/groups'
    try:
        result = requests.get(url, headers=headers)
        status_code = result.status_code
        if status_code == 200:
            return result.json()
        else:
            print("Error fetching groups for user " + user_id + ": " + result.text)
            return None
    except requests.exceptions.RequestException as e:
        print("Error fetching groups for user " + user_id + ":", e)

def remove_user_from_group(user_id, group):
    group_id = group['id']
    group_name = group['profile']['name']
    print("Removing user " + user_id + " from group " + group_id + " (" + group_name + ")")
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'SSWS ' + OKTA_KEY}
    try:
        result = requests.delete('https://' + domain + '/api/v1/groups/' + group['id'] + '/users/' + user_id, headers=headers)
        status_code = result.status_code
        if status_code == 204:
            print("User " + user_id + " removed from group " + group_id + " (" + group_name + ") successfully")
        else:
            print("User " + user_id + " remove from group " + group_id + " (" + group_name + ") failed: " + result.text)
    except requests.exceptions.RequestException as e:
        print("Error removing user from group:", e)

def __action_user(user_id, action):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': 'SSWS ' + OKTA_KEY}
    if action == "activate" or action == "deactivate":
        try:
            result = requests.post('https://' + domain + '/api/v1/users/' + user_id + "/lifecycle/" + action, headers=headers)
            status_code = result.status_code
            if status_code == 200:
                print("User " + user_id + " " + action + "d successfully")
            else:
                print("User " + user_id + " " + action + " failed: " + result.text)
        except requests.exceptions.RequestException as e:
            print("Error " + action + "ing user:", e)
    elif action == "delete":
        try:
            result = requests.delete('https://' + domain + '/api/v1/users/' + user_id, headers=headers)
            status_code = result.status_code
            if status_code == 204:
                print("User " + user_id + " deleted successfully: " + result.text)
            else:
                print("User " + user_id + " delete failed: " + result.text)
        except requests.exceptions.RequestException as e:
            print("Error activating user:", e)
def deactivate_user(user_id):
    __action_user(user_id, "deactivate")
def activate_user(user_id):
    __action_user(user_id, "activate")
def delete_user(user_id):
    __action_user(user_id, "delete")

parser = argparse.ArgumentParser(description='Deactivate user(s) in Okta')
parser.add_argument('--domain', required=True, help='Okta domain, e.g. mycompany.okta.com')
parser.add_argument('--userids', metavar='<user id>', nargs='*', help='1 or more okta user ids that should be deactivated', required=True)
parser.add_argument('--api-token', required=True, help='Okta API key')
parser.add_argument('--action', required=True, type=str, choices=['activate', 'deactivate', 'delete'], help='Set the action: activate, deactivate or delete')
parser.add_argument('--remove-group-membership', required=False, action='store_true', default=False, help='When deactivating a user, remove them from all groups first')
args = parser.parse_args()

OKTA_KEY = args.api_token
user_ids = args.userids
action = args.action
domain = clean_url(args.domain)
remove_group_membership = args.remove_group_membership

if action == "delete":
    print("Please note: only deactivated users will be deleted. If a user is still active, this call will deactivate instead of delete.")
if remove_group_membership:
    print("Please note: A user can't be deleted from builtin groups like \"Everyone\"., this call will error on those groups")

for idx, user_id in enumerate(user_ids):
    if action == "deactivate":
        if remove_group_membership:
            groups = fetch_groups(user_id)
            if groups is not None:
                for group in groups:
                    remove_user_from_group(user_id, group)
        deactivate_user(user_id)
    elif action == "activate":
        activate_user(user_id)
    elif action == "delete":
        delete_user(user_id)