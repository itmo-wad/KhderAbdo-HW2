from flask import Flask, render_template, url_for, redirect, request, session
import datetime
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

data = {"Github": "https://github.com/KhderAbdo", "owner": "Khder Abdo", "version": "1.0.0.1"}

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['lab2']
accounts_collection = db['accounts']

@app.route('/')
def login_get():
    return render_template('login.html', data=data,error=404)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', data=data, error=404)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # find user
        user = accounts_collection.find_one({'username': username, 'password': password})

        if user:
            session['username'] = username
            return redirect(url_for('get_profile'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', data=data, error=404)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login_get'))

@app.route('/register/')
def register_form():
    return render_template('registeration.html', data=data)

@app.route('/register/', methods=['POST'])
def register():
    # Get user data from the registration form
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    university = request.form['university']

    user = accounts_collection.find_one({'username': username})
    if user:
        return 'Username already exists!'
    user = accounts_collection.find_one({'email': email})
    if user:
        return 'Email already exists!'

    # Insert the user data into the database
    new_user = {
        'username': username,
        'password': password,
        'email': email,
        'university': university
    }
    accounts_collection.insert_one(new_user)

    return redirect(url_for('login_get'))

@app.route('/profile/')
def get_profile():
    if 'username' in session:
        account = {"email" : "khder96ju@gmail.com", "address": "ST Petersburg, Lensoveta 23"
        , "hobbies": "football, basketball, reading books",
         "job" : "technical support", "skill" : "HTML, CSS and Java Script"}
        Github = "https://github.com/KhderAbdo"
        Lab1deadline = datetime.datetime.strptime('2024/02/26 11:00', "%Y/%m/%d %H:%M")
        Lab1time_before_deadline = Lab1deadline - datetime.datetime.now().replace(microsecond=0)
        data = {"name" : "Khder", "Github" : Github
            , "Lab1deadline" : Lab1deadline, "Lab1time_before_deadline" : Lab1time_before_deadline,
                "owner" : "Khder Abdo", "version" : "1.0.0.1","account":account
                }
        return render_template("index.html", data=data)
    else:
        return redirect(url_for('login_get'))
