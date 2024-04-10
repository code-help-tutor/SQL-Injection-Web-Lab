# SQL Injection Web Lab

## Introduction

EvanAuth is a brand new startup out of UC Berkeley offering an authentication system. Unfortunately, their new intern has made a mistake and created a SQL injection vulnerability which will allow any user to change another user's password! **Your goal is to change the admin account's password to a known value so you can log into it.**

## Setup + Running

1. Create a virtualenv: `python3 -m venv .161venv`

2. Activate the virtualenv: 
    1. On Mac: `source .161venv/bin/activate`
    2. On Windows: `.\161venv\Scripts\activate`

3. Update `pip` with `python3 -m pip install --upgrade pip`.

4. Install the Python requirements: `pip install -r requirements.txt`

5. Run the server with `./server.sh`


## Instructions:

1. Follow the instructions above to set up and run the server locally.

2. Navigate to http://127.0.0.1:5000 and poke around the website a little. **Note: everytime you restart the server it resets the database to its original state!**

3. Figure out the SQL Injection vulnerability! Your goal is to log into the account with the username "admin". As you complete the SQL injection, note down the various inputs you fed into the website so you can use them for step 4. (Hint: since the source code is open to you it will be helpful to look into it. Check out `main.py` which has the relevant functions marked with a comment, as well as `schema.sql` for the DB table setup). It may also be helpful to read up on [query parameterization in `sqlite3`](https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries).

4. Place your inputs in order in the `input.in` file following the example in `example_input.in`. The first item on every line should be either `Create_Account`, `Login`, `Initiate_Reset`, or `Reset` and determines what call to make to the server based on the 4 types of inputs in the  website (`Initiate_Reset` corresponds to the form on the homepage and `Reset` corresponds to the actual reset password form). Arguments come after and are separated with the `|` character. Do not include the `|` character in any of your arguments (it's not necessary to use it anywhere). To see what arguments each option takes look at `example_input.in`.

5. To test your solution: rerun the server via `./server.sh` to reset its database, then leave it running and **open a second terminal window** to run `python3 grader.py`

## Debugging

It may be difficult to visualize the results of your injected query. To do this we would recommend adding in a print statement after the relevant `conn.execute` statement in `main.py` to print its output. Make sure to rerun the server when you do this so your changes will be reflected.

You can also test SQL queries on the database directly as follows:

1. Open a new terminal window and activate the `venv` by following step 2 in **Setup + Running**.
2. Run `python3`
3. In the interpreter that opens run something similar to the following to execute a query:
```
>>> import sqlite3
>>> conn = sqlite3.connect('database.db')
>>> conn.row_factory = sqlite3.Row
>>> res = conn.execute("SELECT username from users").fetchall()
>>> res[0]['username']
'admin'
```# SQL Injection Web Lab

# 程序代做代写 CS编程辅导

# WeChat: cstutorcs

# Email: tutorcs@163.com

# CS Tutor

# Code Help

# Programming Help

# Computer Science Tutor

# QQ: 749389476
