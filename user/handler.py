from uuid import uuid4

from framework.http.request import Request
from framework.http.responses import JsonResponse

USERS = []

def create_user(request: Request):
    req_data = request.body

    req_data["user_id"]  = uuid4()

    USERS.append(req_data)

    return JsonResponse(data=request.body)


def get_user_list(request:Request):
    return JsonResponse(data={"message": "Hello, World!"})
