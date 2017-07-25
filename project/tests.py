import unittest

from playhouse.test_utils import test_database
from peewee import *

from journalist import app
from models import User, Journal, Tag


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

class FormsTestCase(unittest.TestCase):

    def setUp(self):
            self.tester = app.test_client(self)
            # fake_user = User.create_user(
            #     username='fakeguy',
            #     email='fake@fakeguy.com',
            #     password='password')

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

    # def test_valid_login(self):
    #     with test_database(TEST_DB, (User,)):
    #         response = self.tester.post('/login',
    #             data=dict(
    #                 username=fake_user.username,
    #                 email=fake_user.email,
    #                 password=fake_user.password),
    #                 follow_redirects=True)
    #         self.assertIn(b"Hello", response.data)

    # def test_invalid_login(self):
    #     with test_database(TEST_DB, (User,)):
    #         response = self.tester.post('/login',
    #             data=dict(
    #                 username=fake_user.username,
    #                 email=fake_user.email,
    #                 password='differentpassword'),
    #                 follow_redirects=True)
    #         self.assertIn(b"The username or password you entered is incorrect",
    #                       response.data)

    # def tearDown(self):
    #     get_user = models.User.get(models.User.username == 'fakeguy')
    #     get_user.delete_instance()


if __name__ == '__main__':
    unittest.main()
