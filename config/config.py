import os


class Config(object):
    """
    The superclass to all configuration classes.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URL = os.environ['DATABASE_URL']

class ProductionConfig(Config):
    """
    Production configurations.
    """
    DEBUG = False


class StagingConfig(Config):
    """
    Staging configurations.
    """
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations.
    """
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configurations.
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    test_db = os.path.join(directory, '../tests/test.db')

    TESTING = True
    DATABASE_URL = 'sqlite:///' + test_db