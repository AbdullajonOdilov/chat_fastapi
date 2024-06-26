from fastapi import HTTPException


def role_verification(user, function):
    # allowed_functions_for_users = [""]
    if user.role == "admin" or user.role == "user":
        return True
    # elif user.role == "user" and function in allowed_functions_for_users:
    #     return True
    raise HTTPException(status_code=400, detail='You are not allowed!')

