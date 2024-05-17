import pytest
from pypinnacle.app import PyPinnacle


@pytest.fixture
def app():
    return PyPinnacle()


@pytest.fixture
def test_client(app):
    return app.test_session()
