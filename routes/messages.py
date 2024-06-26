import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.messages import all_messages, create_message, one_message, update_message, delete_message

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemas.messages import CreateMessage, UpdateMessage
from db import database

from schemas.users import UserCurrent
message_router = APIRouter(
    prefix="/messages",
    tags=["Messages operation"]
)


@message_router.post('/create', )
async def message_create(form: CreateMessage, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    await create_message(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Successfully performed")


@message_router.get('/', status_code=200)
def get_messages(search: str = None,  id: int = 0, page: int = 1,
              limit: int = 25, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    if id:
        return one_message(db, id)
    else:
        role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_messages(search=search,  page=page, limit=limit, db=db)


@message_router.put("/update")
def message_update(form: UpdateMessage, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_message(form, db)
    raise HTTPException(status_code=200, detail="Successfully performed")


@message_router.delete("/delete")
def message_delete(id, db: Session = Depends(database),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    delete_message(id, db, current_user)
    raise HTTPException(status_code=200, detail="Successfully deleted")





