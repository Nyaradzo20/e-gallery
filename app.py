from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import re
import os

app = Flask(__name__)

app.secret_key = 'bezel'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Katman'
app.config['MYSQL_PASSWORD'] = 'Katman?1997'
app.config['MYSQL_DB'] = 'Users'

mysql = MySQL(app)


@app.route('/')
def  homePage():
    """
    this page should include the sell out,
    its the page that tell our visitors about the app.
    and give the options to signin or signup.
    """
    return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstname' in request.form and 'lastname' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE email = %s', (email, ))
        user = cursor.fetchone()
        
        if user:
            msg = 'account already exist !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email or not firstname or not lastname:
            msg = 'please fill out the form'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s, % s, % s)', (firstname, lastname, username, email, password, ))
            mysql.connection.commit()
            msg =  'you have successfully registered'
    elif request.method == 'POST':
        msg = 'please fill out the form!'
    return render_template('register.html', msg = msg)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            msg = 'logged in successfully !'
            login.email = request.form['email']
            return render_template('home_page.html', msg = msg)
        else:
            msg = 'Incorrect email / password, please try again !'
    return render_template('sign_in.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


  
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dispay')
def display():
    email = login.email
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM userData WHERE email = %s', email)
    data = cursor.fetchall() #{[id:1], [email: admin@example.com],[photo:palace.jpg],[bio: xxxxxxxxx]}
    photo = data.photo
    bio = data.bio 
    return render_template('home_page.html', photo = photo, bio = bio)


@app.route('/uploads', methods=['POST'])
def uploads ():
    msg = ''
    if 'file' not in request.form and 'bio' not in request.form:
        msg = 'please select an image file and write your bio !'
    file = request.files['file']
    bio = request.form['bio']
    if file.filename == '':
        msg = 'No file selected to upload'
    if bio == '':
        msg = 'please write the bio !'
    if file and allowed_file(file.filename):
        photo = secure_filename(file.filename)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO userData VALUES(NULL, %s, %s, %s)', (login.email, photo, bio))
        mysql.connection.commit()
        msg = 'you have successful added a memory!'
        return render_template('home_page.html', msg = msg)
    else:
        msg = "Allowed image types are - png, jpg, jpeg, gif"
    return redirect(request.url, msg = msg)

    
    
if __name__ == "__main__":
    app.run(debug=True)