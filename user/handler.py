from uuid import uuid4

from framework.http.request import Request
from framework.http.responses import JsonResponse

USERS = []


def create_user(request: Request):
    req_data = request.body

    req_data["user_id"] = str(uuid4())

    USERS.append(req_data)
    return JsonResponse(data=req_data)


def get_user_obj(request: Request, user_id):

    for user in USERS:
        if user["user_id"] == user_id:
            return JsonResponse(data={"users": user})

    return JsonResponse(data={"message": "User not found"})


def get_all_user(request: Request):
    return JsonResponse(data={"data": USERS})


def update_user(request: Request, user_id):
    req_data = request.body
    for user in USERS:
        if user["user_id"] == user_id:
            user.update(req_data)
            return JsonResponse(data={"message": "User updated", "user": user})
    return JsonResponse(data={"message": "User not found"})


def delete_user(request: Request, user_id):
    for idx, user in enumerate(USERS):
        if user["user_id"] == user_id:
            deleted_user = USERS.pop(idx)
            return JsonResponse(data={"message": "User deleted", "user": deleted_user})
    return JsonResponse(data={"message": "User not found"})
