class ProductionConfig:
    SECRET_KEY = 'this is the secret key for the production app'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig:
    SECRET_KEY = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True