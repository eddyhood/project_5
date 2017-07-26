import unittest

from flask_login import current_user
from playhouse.test_utils import test_database
from peewee import *

from journalist import app
from models import User, Journal


TEST_DB = SqliteDatabase(':memory:')

class TemplatesTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)

    # Ensure that flask was set up correctly
    def test_index_200_response(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Make sure index template renders as expected
    def test_index_render(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertIn(b'Welcome to Journalist', response.data)

    # Make sure registration template renders as expected
    def test_registration_render(self):
        response = self.tester.get('/register', content_type='html/text')
        self.assertIn(b'Register Here', response.data)

    # Ensure that login template renders as expected
    def test_login_render(self):
        response = self.tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please Login Below' in response.data)

    def test_add_entry_render(self):
        response = self.tester.get('/entry', content_type='html/text')
        self.assertTrue(b'Add a New Journal Entry!' in response.data)

    # def test_detail_render(self):
    #     response = self.tester.get('/details', content_type='html/text')
    #     self.assertTrue(b'Entry Summary' in response.data)

class FormsTestCase(unittest.TestCase):

    def setUp(self):
            self.tester = app.test_client(self)

    # Ensure that registration works when a user enters valid credentials
    def test_valid_registration(self):
        with test_database(TEST_DB, (User,)):
            response = self.tester.post('/register',
                data=dict(
                    username='fake_register',
                    email='fake@register.com',
                    password1='registerpassword123',
                    password2='registerpassword123'),
                    follow_redirects=True)
            self.assertIn(b"successfully registered!", response.data)

    def test_invalid_registration(self):
        with test_database(TEST_DB, (User,)):
            response = self.tester.post('/register',
                data=dict(
                    username='fake_register',
                    email='fake@register.com',
                    password1='registerpassword123',
                    password2='passwordmismatch'),
                    follow_redirects=True)
            self.assertIn(b"Passwords must match", response.data)

    def test_valid_login(self):
        """Test to see if login / validation is working. Uses default admin
        credentials created in journalist.py"""
        response = self.tester.post('/login',
            data=dict(
                username='admin',
                password='admin123!'),
                follow_redirects=True)
        self.assertIn(b"Hello", response.data)

    def test_invalid_login(self):
        """Tests to see if bad login credentials get rejected"""
        response = self.tester.post('/login',
            data=dict(
                username='asljweoj4',
                password='adsfasdf'),
                follow_redirects=True)
        self.assertIn(b"The username or password you entered is incorrect",
                      response.data)

    def test_logout(self):
        """Test to see if logout works as expecgted"""
        login_user = self.tester.post('/login',
            data=dict(
                username='admin',
                password='admin123!'),
                follow_redirects=True)
        logout_user = self.tester.get('/logout', follow_redirects=True)
        self.assertIn(b"You&#39;ve been logged out", logout_user.data)

class JournalEntryTestCase(unittest.TestCase):
    """Test the views related to adding, editing, and deleting entries"""

    def setUp(self):
        self.tester = app.test_client(self)
        login_user = self.tester.post('/login',
        data=dict(
            username='admin',
            password='admin123!'),
            follow_redirects=True)

    def test_valid_add_entry(self):
        response=self.tester.post('/entry',
            data=dict(
                user=current_user,
                title='Fake Journal Entry',
                date='07/31/2017',
                time=50,
                entry='Fake entry here',
                resources='Fake resources',
                tag='Fake Tag'), follow_redirects=True)
        self.assertIn(b'Your entry was recorded!', response.data)

    def test_invalid_date_add_entry(self):
        response=self.tester.post('/entry',
            data=dict(
                user=current_user,
                title='Fake Journal Entry',
                date='07-31-2017',
                time=50,
                entry='Fake entry here',
                resources='Fake resources',
                tag='Fake Tag'), follow_redirects=True)
        self.assertIn(b'Enter the date as MM/DD/YYYY', response.data)

    def test_invalid_time_add_entry(self):
        response=self.tester.post('/entry',
            data=dict(
                user=current_user,
                title='Fake Journal Entry',
                date='07/31/2017',
                time='50 minutes',
                entry='Fake entry here',
                resources='Fake resources',
                tag='Fake Tag'), follow_redirects=True)
        self.assertIn(b'Enter a number value only for time spent', response.data)

    def cleanUp(self):
        get_entry = Journal.get(Journal.title == 'Fake Journal Entry')
        get_entry.delete_instance()
        logout_user = self.tester.get('/logout', follow_redirects=True)



if __name__ == '__main__':
    unittest.main()
