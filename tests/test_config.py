import os

def test_development_config(app):
    app.config.from_object('app.config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///WMGTSS.db'
    
def test_testing_config(app):
    app.config.from_object('app.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///WMGTSS.db'

def test_production_config(app):
    app.config.from_object('app.config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://qtcllstuqtgix8mi:ckcs304toki4fkvb@yvu4xahse0smimsc.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/ap7ehx04x2fx13c4'
