import pytest
from app import app

@pytest.fixture
def app():
    app.config.from_object('project.config.TestingConfig')
    return app