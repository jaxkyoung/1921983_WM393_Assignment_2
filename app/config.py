class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tmp/WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True