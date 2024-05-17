from typing import Any
from webob import Response as WebobResponse
import json


class Response:

    def __init__(self) -> None:
        self.status_code = 200
        self.body = b""
        self.text = None
        self.json = None
        self.html = None
        self.content_type = "text/plain"

    def set_body_and_content_type(self):
        if self.json:
            self.body = json.dumps(self.json).encode()
            self.content_type = "application/json"
        elif self.html:
            self.body = self.html.encode()
            self.content_type = "text/html"
        elif self.text:
            self.body = self.text.encode()
            self.content_type = "text/plain"

    def __call__(self, environ, start_response):
        self.set_body_and_content_type()

        response = WebobResponse(
            body=self.body,
            status=self.status_code,
            content_type=self.content_type,
        )
        return response(environ, start_response)
