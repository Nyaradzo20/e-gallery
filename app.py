import os
from flask import Flask, render_template, request, redirect, url_for
#from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'mysql://root:Katman1997@127.0.0.1:3306/Users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    email = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.firstname}>'


@app.route('/')
def first_page():
    """
    this page should include the sell out,
    its the page that tell our visitors about the app.
    and give the options to signin or signup.
    """
    return render_template('index.html')

@app.route('/signup')
def signUP ():
    """
    this is the sign up page for new users.
    """
    return render_template('sign_up.html')

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