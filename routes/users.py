import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.users import user_create, update_user, all_users, one_user

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.users import CreateUser, UpdateUser
from db import database

from schemas.users import UserCurrent
users_router = APIRouter(
    prefix="/users",
    tags=["Users operation"]
)


@users_router.post('/create', )
def create_user(form: CreateUser, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)
                ):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    user_create(form=form, db=db)
    raise HTTPException(status_code=200, detail="Successfully performed")


@users_router.get('/', status_code=200)
def get_users(search: str = None,  id: int = 0, role: str = None, page: int = 1,
              limit: int = 25, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    if id:
        return one_user(db, id)
    else:
        role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_users(search=search, role=role, page=page, limit=limit, db=db, )


@users_router.put("/update")
def user_update(form: UpdateUser, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_user(form, db)
    raise HTTPException(status_code=200, detail="Successfully performed")


