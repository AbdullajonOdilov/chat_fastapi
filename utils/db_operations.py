from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db import Base, database


def get_in_db(
        db: Session,
        model,
        ident: int
):
    obj = db.query(model).get(ident)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is no {model}"
        )
    return obj


def save_in_db(
        db: database,
        obj: Base
):
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def the_one(db, model, id):
    the_one = db.query(model).filter(model.id == id).first()
    if not the_one:
        raise HTTPException(status_code=400, detail=f"There is no {model} !")
    return the_one


def the_one_username(db, model, username):
    the_one = db.query(model).filter(model.username == username,).first()
    if the_one:
        raise HTTPException(status_code=400, detail=f"This ({username}) exists!")
    return the_one


def the_one_model_name(db, model, name):
    the_one = db.query(model).filter(model.name == name).first()
    if the_one:
        raise HTTPException(status_code=400, detail=f"This ({name}) exists!")
    return the_one

