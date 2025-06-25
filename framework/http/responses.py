import json

from .request import Request
from .status import HTTP_200_OK, HTTP_STATUS_REASONS


class BaseResponse:

    content_type = None

    def __init__(self, data=None, status_code=None, headers=None):
        self.data = data
        self.headers = headers or {}
        self.status_code = status_code

    def set_header(self, key, value):
        self.headers[key] = value

    def to_response(self, request:Request):
        raise NotImplementedError("Subclasses should implement this method.")

    def to_http_response(self, request:Request):

        response = f"{request.http_version} {self.status_code} {HTTP_STATUS_REASONS.get(self.status_code)}\r\n"

        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"

        response += "\r\n"

        return response



class JsonResponse(BaseResponse):
    content_type = "application/json"

    def __init__(self, data=None, status_code=HTTP_200_OK, headers=None):
        super().__init__(data=data, status_code=status_code, headers=headers)

    def to_response(self, request:Request):

        response_data = json.dumps(self.data) if self.data else "{}"

        self.set_header("Content-Type", self.content_type)
        self.set_header("Content-Length", str(len(response_data)))

        return self.to_http_response(request) + response_data

