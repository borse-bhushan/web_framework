from ..http.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class BaseException(Exception):
    """Base class for all exceptions in the framework."""

    status_code = HTTP_500_INTERNAL_SERVER_ERROR  # Default HTTP status code for server errors

    message: str = "An error occurred"

    def __init__(self, message: str = None, *args):
        super().__init__(*args)

        self.message = message or self.message




class NotFoundException(BaseException):
    """Exception raised when a requested resource is not found."""

    status_code = HTTP_404_NOT_FOUND
    message: str = "Resource not found"



class ContentTypeException(BaseException):
    """Exception raised when the content type is not supported."""

    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "Unsupported content type"
