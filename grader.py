WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
import re
import requests
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

BASE_URL = "http://127.0.0.1:5000"
ADMIN_PASS_HASH = ""

reset_id = ''

def create_account(args):
    if len(args) != 2:
        raise Exception("Invalid number of arguments, should be 2.") 
    return requests.post(BASE_URL + "/create", {"username": args[0], "password": args[1]})

def login(args):
    if len(args) != 2:
        raise Exception("Invalid number of arguments, should be 2.") 
    return requests.post(BASE_URL + "/login", {"username": args[0], "password": args[1]})

def initiate_reset(args):
    if len(args) != 1:
        raise Exception("Invalid number of arguments, should be 1.") 
    res = requests.get(BASE_URL + f"/initiate-reset?username={args[0]}")

    for item in res.iter_lines():
        item = str(item)
        if "reset-id" in item:
            ids = re.findall("value=([0-9]+)", item)
            if len(ids) != 1:
                raise Exception("ERROR: reset form code was tampered with.") 
            global reset_id
            reset_id = ids[0]
    return res

def reset(args):
    global reset_id
    if len(args) != 2:
       raise Exception("Invalid number of arguments, should be 2.")
    if not reset_id:
       raise Exception("Cannot reset without first initiating a reset.") 
    res = requests.post(BASE_URL + "/reset", {"curr-password": args[0], "new-password": args[1], "reset-id": reset_id})
    reset_id = ''
    return res

ACTIONS = {"Create_Account": create_account, "Login": login, "Initiate_Reset": initiate_reset, "Reset": reset}

if __name__ == "__main__":
    connection = get_db_connection()
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.close()

    with open("input.in") as input:
        lines = input.readlines()

        for i, line in enumerate(lines):
            split = line.split("|")
            split = [elem.strip() for elem in split]
            action = split[0].strip()
            if action not in ACTIONS.keys():
                raise Exception(f"Invalid action provided: {action}")
            try:
                ACTIONS[action](split[1:]).iter_lines()
            except Exception as e:
                raise Exception(str(e) + f" on line {i+1}")

        connection = get_db_connection()
        res = connection.execute("SELECT password from users WHERE username='admin'").fetchone()
        connection.close()
        if not res:
            print("FAIL: admin account has been deleted.")
        password = res[0]
        if password == ADMIN_PASS_HASH:
            print("FAIL: admin password was unchanged.")
        else:
            print("SUCCESS")
