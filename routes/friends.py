import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.friends import all_friends, create_friend, one_friend, delete_friend

from routes.login import get_current_active_user
from schemas.friends import CreateFriend
from utils.role_verification import role_verification
from db import database

from schemas.users import UserCurrent

friend_router = APIRouter(
    prefix="/friends",
    tags=["Contacts operation"]
)


@friend_router.post('/create', )
def friend_create(form: CreateFriend, db: Session = Depends(database),
                  current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_friend(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Successfully performed")


@friend_router.get('/', status_code=200)
def get_friends(id: int = 0, page: int = 1,
                 limit: int = 25, db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    if id:
        return one_friend(db, id)
    else:
        role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_friends(page=page, limit=limit, db=db)



@friend_router.delete("/delete")
def message_friend(id, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_friend(id, db)
    raise HTTPException(status_code=200, detail="Successfully deleted")





