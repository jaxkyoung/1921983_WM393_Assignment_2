class ProductionConfig:
    SECRET_KEY = 'this is the secret key for the production app'
    SQLALCHEMY_DATABASE_URI = 'mysql://qtcllstuqtgix8mi:ckcs304toki4fkvb@yvu4xahse0smimsc.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/ap7ehx04x2fx13c4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig:
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False

class TestingConfig:
    SECRET_KEY = 'test'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///WMGTSS.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True