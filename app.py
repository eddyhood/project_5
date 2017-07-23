from flask import (Flask, request, session, g, redirect, url_for,
                   render_template, flash)
from flask_bcrypt import Bcrypt, check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
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

#Wrap the app in CSRF protection for forms
csrf =CSRFProtect(app)

#Configure login
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """Creates a session when the user logs in"""
    try:
        models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        pass


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
        flash("You've successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LogInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash('The username or password you entered is incorrect')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Hello {}!'.format(user.username), "success")
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT, host=HOST)

