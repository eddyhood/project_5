import unittest

import app
from models import User, Journal, Tag


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.fake_user = User.create_user(
                                username='fake_$_user',
                                email='fake@fakeemail.com',
                                password='password'
                                )
        self.fake_journal = Journal.create(
                                user=1,
                                title='fake journal entry',
                                date=07/29/1980,
                                time=100,
                                entry="I have learned a lot.",
                                resources="Take more Treehouse courses")
        self.fake_tag = Tag.create(
                            journal=1,
                            tag='fake_tag')

    def test_create_user(self):
        """See of a user was created in the setup """
        self.assertTrue(User.get(User.username == 'fake_$_user'))

    def test_create_duplicate_user(self):
        """Try to create a duplicate user and see if ValueError is raised """
        with self.assertRaises(ValueError):
            User.create_user(
                    username='fake_$_user',
                    email='fake@fakeemail.com',
                    password='password'
                    )

    def test_password_hash(self):
        """See if the password was hashed or if it stayed 'password' """
        self.assertNotEqual(User.select().get().password, 'password')

    def test_create_journal(self):
        """See of a journal was created in the setup """
        self.assertTrue(Journal.get(Journal.title == 'fake journal entry'))

    def test_create_tag(self):
        """See of a tag was created in the setup """
        self.assertTrue(Tag.get(Tag.tag == 'fake_tag'))

    def tearDown(self):
        User.get(User.username='fake_$_user').delete_instance()
        Journal.get(Journal.title='fake journal entry').delete_instance()
        Tag.get(Tag.tag='fake_tag').delete_instance()


