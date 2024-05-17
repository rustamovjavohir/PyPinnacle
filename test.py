import pytest
import requests
import wsgiadapter
from conftest import app, test_client
from pypinnacle.middleware import Middleware


def test_basic_route_adding(app):

    @app.route("/home")
    def home(request, response):
        response.text = "Home"

    assert app.routes["/home"].get("handler") == home


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


def test_alternative_route(app, test_client):

    def home(request, response):
        response.text = "From new home handler"

    app.add_route("/home", home)

    response = test_client.get("http://testserver/home")

    assert response.status_code == 200
    assert response.text == "From new home handler"


def testt_template_handler(app, test_client):

    @app.route("/template")
    def template_handler(request, response):
        response.body = app.template(
            "home.html",
            context={"title": "PyPinnacle", "body": "This is a template"},
        )
        response.content_type = "text/html"

    response = test_client.get("http://testserver/template")

    assert response.status_code == 200
    assert "PyPinnacle" in response.text
    assert "This is a template" in response.text
    assert "text/html" in response.headers["Content-Type"]


def test_custom_exeption_handler(app, test_client):

    def on_exception(request, response, exc):
        response.text = "Oops! Something went wrong."
        # response.text = str(exc)

    app.add_exception_handler(on_exception)

    @app.route("/exception")
    def exception_throwing_handler(request, response):
        raise AttributeError("This handler should not be used")

    response = test_client.get("http://testserver/exception")
    assert response.text == "Oops! Something went wrong."


def test_non_existent_static_file(test_client):
    assert test_client.get("http://testserver/static/main.css").status_code == 404


def test_serving_static_file(test_client):
    response = test_client.get("http://testserver/static/test.css")

    assert response.status_code == 200

    assert response.text == "body {background-color: #f0f0f0;}"


def test_middleware_method_call(app, test_client):
    process_request_called = False
    process_response_called = False

    class TestMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, request):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, request, response):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(TestMiddleware)

    @app.route("/home")
    def home(request, response):
        response.text = "Home"

    response = test_client.get("http://testserver/home")

    assert process_request_called == True
    assert process_response_called == True
    assert response.status_code == 200


def test_allowed_methods_for_function_based_handlers(app, test_client):

    @app.route("/home", allowed_methods=["post"])
    def home(request, response):
        response.text = "Home"

    response = test_client.get("http://testserver/home")

    assert response.status_code == 405
    assert response.text == "Method Not Allowed GET"


def test_json_response_helper(app, test_client):

    @app.route("/json")
    def json_handler(request, response):
        response.json = {"name": "PyPinnacle", "language": "Python"}

    response = test_client.get("http://testserver/json")
    response_data = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert response_data == {"name": "PyPinnacle", "language": "Python"}


def test_text_response_helper(app, test_client):

    @app.route("/text")
    def text_handler(request, response):
        response.text = "This is a plain text"

    response = test_client.get("http://testserver/text")

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "This is a plain text"


def test_html_response_helper(app, test_client):

    @app.route("/html")
    def html_handler(request, response):
        response.html = app.template(
            "home.html",
            context={"title": "PyPinnacle", "body": "This is a template"},
        )

    response = test_client.get("http://testserver/html")

    assert "text/html" in response.headers["Content-Type"]
    assert "PyPinnacle" in response.text