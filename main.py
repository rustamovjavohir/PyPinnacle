from app import PyPinnacle

app = PyPinnacle()


@app.route('/home')
def home(request, response):
    response.text = "Hello from the Home Page"


@app.route('/about')
def about(request, response):
    response.text = "Hello from the About Page"


@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f"Hello {name}"
