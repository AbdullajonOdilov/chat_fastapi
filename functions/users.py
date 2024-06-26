from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.friends import Friends
from routes.login import get_password_hash
from utils.db_operations import the_one, the_one_username, save_in_db
from utils.pagination import pagination
from models.users import Users


def all_users(search, role, page, limit, db):
    users = db.query(Users)

    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.username.like(search_formatted))
    if role:
        users = users.filter(Users.role == role)
    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)


def user_create(form, db):
    the_one_username(db=db, model=Users, username=form.username)
    if form.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Role error, please try user and admin")
    new_user_db = Users(
        fullname=form.fullname,
        username=form.username,
        role=form.role,
        password_hash=get_password_hash(form.password_hash))

    save_in_db(db, new_user_db)
    raise HTTPException(status_code=200, detail=f"Successfully created")


def one_user(db, id):
    the_item = db.query(Users).filter(Users.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="Not found")


def update_user(form, db):
    user = the_one(db=db, model=Users, id=form.id)
    if db.query(Users).filter(Users.username == form.username).first() and user.username != form.username:
        raise HTTPException(status_code=400, detail="The data exists")
    if form.password_hash == "":
        db.query(Users).filter(Users.id == form.id).update({
            Users.fullname: form.fullname,
            Users.username: form.username,
            Users.password: user.password,
            Users.password_hash: get_password_hash(user.password),
            Users.role: form.role,
        })
    db.commit()
