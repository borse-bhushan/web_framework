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
        """
        Sets or updates a header in the response.
        Args:
            key (str): The name of the header to set.
            value (str): The value to assign to the header.
        """

        self.headers[key] = value

    def to_response(self, request: Request):
        raise NotImplementedError("Subclasses should implement this method.")

    def to_http_response(self, request: Request):
        """
        Converts the response object into a raw HTTP response string.
        Args:
            request (Request): The HTTP request object containing information such as the HTTP version.
        Returns:
            str: A string formatted as a raw HTTP response, including the status line, headers, and a blank line separating headers from the body.
        Notes:
            - The response string does not include the response body.
            - The status reason phrase is retrieved from HTTP_STATUS_REASONS using the status code.
            - Headers are included as key-value pairs, each on a new line.
        """

        response = f"{request.http_version} {self.status_code} {HTTP_STATUS_REASONS.get(self.status_code)}\r\n"

        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"

        response += "\r\n"

        return response


class JsonResponse(BaseResponse):
    content_type = "application/json"

    def __init__(self, data=None, status_code=HTTP_200_OK, headers=None):
        super().__init__(data=data, status_code=status_code, headers=headers)

    def to_response(self, request: Request):
        """
        Converts the current response object into a complete HTTP response string.
        This method serializes the response data to JSON (if present), sets the appropriate
        HTTP headers (such as Content-Type and Content-Length), and combines the HTTP response
        headers with the serialized response body.
        Args:
            request (Request): The incoming HTTP request object.
        Returns:
            str: The full HTTP response as a string, including headers and body.
        """

        response_data = json.dumps(self.data) if self.data else "{}"

        self.set_header("Content-Type", self.content_type)
        self.set_header("Content-Length", str(len(response_data)))

        return self.to_http_response(request) + response_data
