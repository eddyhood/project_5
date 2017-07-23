import datetime

from flask_login import UserMixin
from peewee import *

import app

# Set up a database with Sqlite3
DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
    """Model for creating a new user """
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    created_on = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=app.bcrypt.generate_password_hash(password)
                    )
        except IntegrityError:
            raise ValueError('User already exists')


class Journal(Model):
    """Model for creating a new journal entry """
    user = ForeignKeyField(User, related_name="journal")
    title = CharField(max_length=100)
    date = DateField()
    time = IntegerField()
    entry = TextField()
    resources = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)



class Tag(Model):
    """Model for creating a new tag"""
    journal = ForeignKeyField(Journal, related_name='tag')
    tag = CharField(max_length="20")


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Journal, Tag], safe=True)
    DATABASE.close()

