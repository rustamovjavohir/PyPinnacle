
# PyPinnacle

PyPinnacle is a powerful and flexible Python framework for building web applications quickly and efficiently.

![purpose](https://img.shields.io/badge/purpose-learning-green)

![PyPI - Version](https://img.shields.io/pypi/v/PyPinnacle)


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Simple and intuitive API
- Built-in support for common web functionalities
- Highly extensible and customizable
- Lightweight and fast
- Comprehensive documentation

## Installation

You can install PyPinnacle using pip:

```bash
pip install pypinnacle
```

### Basic usage:
``` python
from pypinnacle.app import PyPinnacle

app = PyPinnacle()

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello {name}"


@app.route("/books")
class Books:

    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"

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
```

### Add middleware
``` python
from pypinnacel.middleware import Middleware
from pypinnacle.app import PyPinnacle

app = PyPinnacle()

class LogMiddleware(Middleware):

    def process_request(self, request):
        print("Processing request", request.url)

    def process_response(self, request, response):
        print("Processing response", request.url)

app.add_middleware(LogMiddleware)  # add middleware
```