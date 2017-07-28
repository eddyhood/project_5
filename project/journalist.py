from datetime import datetime

from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import Bcrypt, check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from flask_wtf.csrf import CSRFProtect

import forms
import models


# Establish the Flask journalist
app = Flask(__name__)
app.config.from_object('config.TestConfig')

bcrypt = Bcrypt(app)

#Wrap the app in CSRF protection for forms
csrf =CSRFProtect(app)

#Configure login
login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader


def load_user(userid):
    """This funcion is what we use to find users."""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Open a database connection before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.teardown_request
def teardown_request(exception):
    """Close the database connection at the end of each request or error"""
    db =getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    """Renders the homepage"""
    return render_template('index.html')


@app.route('/register', methods=('GET', 'POST'))
def register():
    """Provide a registration page & form to capture new users"""
    form = forms.RegisterForm()
    if form.validate_on_submit():
        models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password1.data
                )
        flash("You've successfully registered! Please login below.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Provides a login page for users to get authenticated"""
    form = forms.LogInForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash('The username or password you entered is incorrect', "Error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Hello {}!'.format(user.username), "success")
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Provides  a logout option for authenticated users"""
    logout_user()
    flash("You've been logged out.", "Success")
    return redirect(url_for('index'))


@app.route('/entry', methods=('GET', 'POST'))
@login_required
def add_entry():
    """Allows a user to add a new entry to the journal"""
    form = forms.AddEntryForm()
    if form.validate_on_submit():
        models.Journal.create(
            user=g.user._get_current_object(),
            title=form.title.data,
            date=form.date.data,
            time=form.time.data,
            entry=form.entry.data,
            resources=form.resources.data,
            tag=form.tag.data)
        flash('Your entry was recorded!', 'success')
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/entries')
@login_required
def entries():
    """List view of all entries"""
    user = g.user._get_current_object()
    entries = models.Journal.select().where(models.Journal.user == user).limit(7)
    return render_template('entries.html', entries=entries)


@app.route('/entries/<entry_title>')
@login_required
def details(entry_title):
    """Allows a user to look at the details of a journal entry"""
    entry = models.Journal.select().where(models.Journal.title == entry_title)
    return render_template('detail.html', entry=entry)


@app.route('/entries/edit/<entry_title>', methods=('GET', 'POST'))
@login_required
def edit(entry_title):
    """Prepopulates a form with original entry and allows user to change
    any field and then resave the entry to the database."""
    entry = models.Journal.get(models.Journal.title == entry_title)
    form = forms.AddEntryForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        entry.title = form.title.data
        entry.date = form.date.data
        entry.time = form.time.data
        entry.entry = form.entry.data
        entry.resources = form.resources.data
        entry.tag = form.tag.data
        entry.save()
        flash('Your entry has been updated!')
        return redirect(url_for('entries'))
    return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/delete/<entry_title>', methods=('GET', 'POST'))
@login_required
def delete(entry_title):
    """Allows a user to delete an entry"""
    entry = models.Journal.get(models.Journal.title == entry_title)
    form = forms.DeleteEntryForm()
    if form.validate_on_submit():
        if form.confirm_message.data == entry.title:
            entry.delete_instance()
            flash('Your entry was deleted', 'successs')
        else:
            flash('Enter the exact title to delete', 'error')
        return redirect(url_for('entries'))
    return render_template('delete.html', form=form, entry=entry)


@app.route('/entries/tag/<tag>')
@login_required
def tagview(tag):
    """Shows all entries for a given tag"""
    get_entries = models.Journal.select().where(models.Journal.tag == tag)
    return render_template('taged.html', entries=get_entries)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='admin',
            email='admin@admin.com',
            password='admin123!'
            )
    except ValueError:
        pass
    app.run()
