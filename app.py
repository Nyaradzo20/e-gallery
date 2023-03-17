import os
from flask import Flask, render_template, request, redirect, url_for,session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import MySQLdb.cursors
import re

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://root:Katman1997@127.0.0.1:3306/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    dateOfBirth = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<Users {self.firstname}>'


@app.route('/')
def first_page():
    """
    this page should include the sell out,
    its the page that tell our visitors about the app.
    and give the options to signin or signup.
    """
    return render_template('index.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'firstname' in request.form and 'lastname' in request.form and 'dateOfBirth' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dateOfBirth = request.form['dateOfBirth']
        cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            db.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    """sign in page for users comming back to the app
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('homePage'))
    return render_template('sign_in.html', error=error)
    

@app.route('/new/upload', methods=['GET', 'POST'])
def uploads ():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
    return("File uploaded successfully")
    
@app.route('/homePage')
def homePage():
    """the page that show the information of the user
    """
    
    return render_template('home_page.html')

if __name__ == "__main__":
    app.run(debug=True)