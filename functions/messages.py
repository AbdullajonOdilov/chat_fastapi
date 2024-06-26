import datetime

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.notifications import manager
from models.users import Users
from schemas.notifications import NotificationSchema
from utils.db_operations import the_one, save_in_db
from utils.pagination import pagination
from models.messages import Messages


def all_messages(search, page, limit, db):
    messages = db.query(Messages)

    if search:
        search_formatted = "%{}%".format(search)
        messages = messages.filter(Messages.description.like(search_formatted) | Users.username.like(search_formatted))

    messages = messages.order_by(Messages.id.desc())
    return pagination(messages, page, limit)


async def create_message(form, db, thisuser):
    receiver = db.query(Users).filter(Users.id == form.receiver_id).first()
    new_message_db = Messages(
        description=form.description,
        sender_id=thisuser.id,
        receiver_id=form.receiver_id,
        time=datetime.datetime.utcnow(),
        seen=False,
    )
    save_in_db(db, new_message_db)

    if new_message_db:
        notification_data = NotificationSchema(
            title="New message!",
            body=f"Hey {receiver.fullname} you have new message!",
            user_id=form.receiver_id,
        )
        await manager.send_user(message=notification_data, user_id=form.receiver_id, db=db)
    raise HTTPException(status_code=200, detail="Successfully performed")

def one_message(db, id):
    the_item = db.query(Messages).joinedload(Messages.sender_messages).filter(Messages.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Not found")


def update_message(form, db):
    the_one(db, Messages, id=form.id)
    db.query(Messages).filter(Messages.id == form.id).update({
        Messages.description: form.description
    })
    db.commit()


def delete_message(id, db, thisuser):
    message = the_one(db, Messages, id)
    if message.sender_id != thisuser.id:
        raise HTTPException(status_code=400, detail="You are not allowed")
    db.query(Messages).filter(Messages.id == id).delete()
    db.commit()

