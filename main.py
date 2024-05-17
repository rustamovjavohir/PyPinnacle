from app import PyPinnacle
from middleware import Middleware
import json

app = PyPinnacle()


@app.route("/home", allowed_methods=["get"])
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route("/about")
def about(request, response):
    response.text = "Hello from the About Page"


@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello {name}"


@app.route("/books")
class Books:

    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


def new_route(request, response):
    response.text = "New Route"


app.add_route("/new", new_route)


@app.route("/template")
def template_handler(request, response):
    response.body = app.template(
        "home.html",
        context={"title": "PyPinnacle", "body": "This is a template"},
    )
    response.content_type = "text/html"


@app.route("/json")
def json_handler(request, response):
    response_data = {"name": "PyPinnacle", "language": "Python"}
    response.body = json.dumps(response_data).encode()
    response.content_type = "application/json"


@app.route("/text")
def text_handler(request, response):
    response.text = "This is a plain text"


def on_exception(request, response, exc):
    # response.text = "Oops! Something went wrong."
    response.text = str(exc)


app.add_exception_handler(on_exception)


@app.route("/exception")
def exception_throwing_handler(request, response):
    raise AttributeError("This handler should not be used")


class LogMiddleware(Middleware):

    def process_request(self, request):
        print("Processing request", request.url)

    def process_response(self, request, response):
        print("Processing response", request.url)


class GettingMiddleware(Middleware):

    def process_request(self, request):
        print("Getting middleware", request.url)

    def process_response(self, request, response):
        print("Getting middleware response", request.url)


# app.add_middleware(LogMiddleware)
# app.add_middleware(GettingMiddleware)
