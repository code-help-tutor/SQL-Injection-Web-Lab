WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
import secrets
import bcrypt
import base64
import hashlib

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__, template_folder="templates")

########################################################################
### THE FUNCTIONS IN THIS BLOCK ARE WHERE THE VULNERABILITY MAY LIE. ###
########################################################################

# A little on Flask syntax:
# @app.route is a decorator that signifies this function is used to respond to a request at a specific endpoint when it is invoked with a set of HTTP methods.
# In this case: create() is the handler function that will be called when a POST request is made at /create/
# Whatever the function returns is what the user of the website will see.
@app.route('/create/', methods=["POST"])
def create():
    conn = get_db_connection()
    salt = bcrypt.gensalt()
    hashed_pass = hash_password(request.form['password'], salt)
    try:
        conn.execute("INSERT INTO users VALUES (?, ?)", (request.form['username'], hashed_pass))
    except sqlite3.IntegrityError:
        conn.close()
        return "Username already in use.", 403
    conn.commit()
    conn.close()
    return render_template("index.html")

@app.route('/login/', methods=['POST'])
def login():
    conn = get_db_connection()
    res = conn.execute("SELECT password FROM users WHERE username=?", (request.form['username'],)).fetchone()
    if res is None:
        return render_template("login_result.j2", username="Nonexistent User", success=False)
    pass_hash = res[0]
    conn.close()
    pass_hash = pass_hash if type(pass_hash) == bytes else bytes(pass_hash, 'utf-8')
    return render_template("login_result.j2", username=request.form['username'], success=bcrypt.checkpw(prep_to_hash(request.form['password']), pass_hash))

@app.route('/initiate-reset/', methods=["GET"])
def initiate_reset():
    reset_id = secrets.randbits(32)
    if 'username' not in request.args or not request.args['username']:
        return "Please submit this form from the homepage with a username.", 403
    conn = get_db_connection()
    conn.execute("INSERT INTO resets VALUES (?, ?)", (reset_id, request.args['username']))
    conn.commit()
    return render_template("reset.j2", username=request.args['username'], reset_id=reset_id)

@app.route('/reset/', methods=["POST"])
def reset_password():
    conn = get_db_connection()
    res = conn.execute(f"SELECT username FROM resets WHERE id=?", (request.form['reset-id'],)).fetchone()
    if not res:
        return "Reset request does not exist.", 404
    username = res[0]
    # Handle password hashing
    new_salt = bcrypt.gensalt()
    hashed_new_password = hash_password(request.form['new-password'], new_salt)
    res = conn.execute("SELECT password FROM users WHERE username=?", (username,)).fetchone()
    if not res:
        return f"User {username} does not exist.", 404
    curr_password_hash = res[0]
    hashed_curr_password_submission = bcrypt.hashpw(prep_to_hash(request.form['curr-password']), curr_password_hash)
    try:
        conn.execute(f"UPDATE users SET password=? WHERE username='{username}' and password=?", (hashed_new_password, hashed_curr_password_submission))
    except sqlite3.ProgrammingError:
        return "Error: The number of parameters passed to the query in conn.execute did not match its number of placeholders. Placeholders in sqlite3 are question marks ('?') and are also referred to as \"bindings\" in the documentation.", 500
    finally:
        conn.commit()
        conn.close()
    # There is no vulnerability within this function call.
    if not did_password_update(username, hashed_new_password):
        return "Incorrect current password entered", 403
    return render_template("login.html")

####################################################
### CODE BELOW HERE IS SETUP AND NOT VULNERABLE. ###
####################################################
@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/login/', methods=["GET"])
def login_form():
    return render_template("login.html")

@app.route('/create/', methods=["GET"])
def create_form():
    return render_template("create_account.html")

def prep_to_hash(password):
    # We sha256 hash first since bcrypt only supports passwords up to 72 characters. Base64 encoding will then prevent null-byte issues.
    return base64.b64encode(hashlib.sha256(password.encode('utf-8')).digest())

def hash_password(password, salt):
    return bcrypt.hashpw(prep_to_hash(password), salt)

def did_password_update(username, new_password):
    connection = get_db_connection()
    res = connection.execute("SELECT password from users WHERE username=?", (username,)).fetchone()
    connection.close()
    if not res:
        return False
    password = res[0]
    return password == new_password

# This function handles database connection setup.
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initializes the database back to its default state.
connection = get_db_connection()
with open('schema.sql') as f:
    connection.executescript(f.read())
connection.close()