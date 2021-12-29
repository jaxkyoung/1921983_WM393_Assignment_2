import os
import sys
import inspect
import pytest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('app.config.TestingConfig')
    return app