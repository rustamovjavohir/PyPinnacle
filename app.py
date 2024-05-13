from webob import Request, Response
from parse import parse


class PyPinnacle:
    def __init__(self) -> None:
        self.routes = dict()

    def __call__(self, environ, start_response):
        request = Request(environ=environ)
        response = self.handle_request(request=request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request)

        if handler:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def find_handler(self, request):
        for path, handler in self.routes.items():
            parsed_result = parse(path, request.path)
            if parsed_result is not None:
                return handler, parsed_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found"

    def route(self, path):

        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper
