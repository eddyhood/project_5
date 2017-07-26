from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, DateField, IntegerField,
                     TextAreaField)
from wtforms.validators import DataRequired, Email, Regexp, Length, EqualTo, InputRequired

import models


def name_exists(form, field):
    """Make sure that someone doesn't register with an existing username"""
    if models.User.select().where(models.User.username == field.data).exists():
        raise ValidationError('User with that username already exists.')


def email_exists(form, field):
    """Make sure that someone doesn't register with an existing username"""
    if models.User.select().where(models.User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
    username = StringField(
                    'Username',
                    validators=[
                        DataRequired(),
                        Regexp(
                            r'^[a-zA-Z0-9_]+$',
                            message=('Username can be letters, numbers, and _')
                            ), name_exists
                    ]
               )

    email = StringField(
                'Email',
                validators=[
                    DataRequired(),
                    Email(),
                    email_exists
                ]
            )

    password1 = PasswordField(
                    'Password',
                    validators=[
                        DataRequired(),
                        Length(min=7,
                               message='Password must be 7+ characters'),
                        EqualTo('password2', message='Passwords must match.')
                    ]
                )

    password2 = PasswordField(
                    'Confirm Password',
                    validators=[
                    DataRequired()
                    ]
                )


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), ])
    password = PasswordField('Password', validators=[DataRequired()])


class AddEntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    date = DateField(
                     'Date as MM/DD/YYYY',
                     validators=[
                     DataRequired(message='Enter the date as MM/DD/YYYY')],
                     format='%m/%d/%Y'
                     )
    time = IntegerField('Time Spent', validators=[DataRequired(
        message='Enter a number value only for time spent')])
    entry = TextAreaField('What You Learned', validators=[DataRequired()])
    resources = TextAreaField('Resources to Remember')
    tag = StringField('Tag')


