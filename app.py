from flask import (Flask, request, session, g, redirect, url_for,
                   render_template, flash)

from flask_bcrypt import Bcrypt, check_password_hash
from flask_wtf.csrf import CSRFProtect

import forms
import models

# Set up configuration for the application
DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

# Establish the Flask app
app = Flask(__name__)
app.secret_key = "alkjwrew/wt,-40[-q34pok34/2;;1120i;434//.,-20391`!!"

#Establish the password hashing system
bcrypt = Bcrypt(app)

#Wrap the app in CSRF protection
csrf =CSRFProtect(app)


@app.before_request
def before_request():
    """Open a database connection before each request"""
    g.db = models.DATABASE
    g.db.connect()



@app.teardown_request
def teardown_request(exception):
    """Close down the database connection at the end of each request or error"""
    db =getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Home page view"""
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password1.data
                )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)

