#default config
class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'alkjwrew/wt,-40[-q34pok34/2;;1120i;434//.,-20391`!!'
    WTF_CSRF_ENABLED = True
    DATABASE_URI = 'sqlite:///journal.db'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_URI = 'sqlite://:memory:'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionCONFIG(BaseConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = True

