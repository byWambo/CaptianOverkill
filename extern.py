import json
import time
import os


def set_report_cd(user_id: int):
    user_id = str(user_id)
    if os.path.isfile("users.json"):
        try:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
                users[user_id]['cooldwon_end'] = int(time.time()) + 604800
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
        except KeyError:
            with open('users.json', 'r') as fp:
                users = json.load(fp)
            users[user_id] = {}
            users[user_id]['cooldwon_end'] = int(time.time()) + 604800
            with open('users.json', 'w') as fp:
                json.dump(users, fp, sort_keys=True, indent=4)
    else:
        users = {user_id: {}}
        users[user_id]['cooldwon_end'] = int(time.time()) + 604800
        with open('users.json', 'w') as fp:
            json.dump(users, fp, sort_keys=True, indent=4)


def get_cooldown_end(user_id: int):
    user_id = str(user_id)
    if os.path.isfile('users.json'):
        with open('users.json', 'r') as fp:
            users = json.load(fp)
        ret_val = True
        try:
            if int(users[user_id]['cooldwon_end']) <= int(time.time()):
                ret_val = True
            else:
                ret_val = False
        except KeyError:
            ret_val = True
        return ret_val
    else:
        return True