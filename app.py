from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/')
def first_page():
    """
    this page should include the sell out,
    its the page that tell our visitors about the app.
    and give the options to signin or signup.
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)