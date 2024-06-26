from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.users import Users
from utils.db_operations import the_one, save_in_db
from utils.pagination import pagination
from models.friends import Friends


def all_friends(page, limit, db):
    friends = db.query(Friends)

    friends = friends.order_by(Friends.id.desc())
    return pagination(friends, page, limit)


def create_friend(form, db, thisuser):
    if thisuser.id == form.friend_id:
        raise HTTPException(status_code=400, detail="User id error")
    new_friend_db = Friends(
        friend_id=form.friend_id,
        user_id=thisuser.id
    )

    save_in_db(db, new_friend_db)
    raise HTTPException(status_code=200, detail=f"Successfully created")


def one_friend(db, id):
    the_item = db.query(Friends).options(joinedload(Friends.friends)).filter(Friends.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Not found")


def delete_friend(id, db):
    the_one(db, Friends, id)
    db.query(Friends).filter(Friends.id == id).delete()
    db.commit()

