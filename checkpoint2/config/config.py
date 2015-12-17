import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URL = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    
    directory = os.path.dirname(os.path.abspath(__file__))
    test_db = os.path.join(directory, '../tests/test.db')

    TESTING = True
    DATABASE_URL = 'sqlite:///' + test_db