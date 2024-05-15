import pytest
import requests
import wsgiadapter
from conftest import app, test_client


def test_basic_route_adding(app):

    @app.route("/home")
    def home(request, response):
        response.text = "Home"

    assert app.routes["/home"] == home


def test_duplicate_routes_throws_exception(app):

    @app.route("/home")
    def home(request, response):
        response.text = "Home"

    with pytest.raises(AssertionError):

        @app.route("/home")
        def home2(request, response):
            response.text = "Home2"


def test_request_can_be_sent_by_test_client(app, test_client):

    @app.route("/home")
    def home(request, response):
        response.text = "Home"

    response = test_client.get("http://testserver/home")

    assert response.status_code == 200
    assert response.text == "Home"


def test_parameterized_route(app, test_client):

    @app.route("/hello/{name}")
    def geeting(request, response, name):
        response.text = f"Hello, {name}"

    response = test_client.get("http://testserver/hello/Javohir")

    assert response.status_code == 200
    assert response.text == "Hello, Javohir"


def test_default_404_response(app, test_client):

    response = test_client.get("http://testserver/404")

    assert response.status_code == 404
    assert response.text == "Not found"


def test_class_based_handler_get(app, test_client):

    @app.route("/home")
    class HomeResource:
        def get(self, request, response):
            response.text = "Home"

    response = test_client.get("http://testserver/home")

    assert response.status_code == 200
    assert response.text == "Home"


def test_class_based_handler_post(app, test_client):

    @app.route("/home")
    class HomeResource:
        def post(self, request, response):
            response.text = "Post request to home"

    response = test_client.post("http://testserver/home")

    assert response.status_code == 200
    assert response.text == "Post request to home"


def test_class_based_handler_not_allowed_method(app, test_client):

    @app.route("/home")
    class HomeResource:
        def post(self, request, response):
            response.text = "Post request to home"

    response = test_client.get("http://testserver/home")

    assert response.status_code == 405
    assert response.text == "Method Not Allowed GET"
