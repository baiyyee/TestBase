import email
from sqlalchemy.orm import Session
from . import model, schema


def get_user(session: Session, user_id: int):
    return session.query(model.User).filter(model.User.id == user_id).first()


def get_user_by_email(session: Session, email: str):
    return session.query(model.User).filter(model.User.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(model.User).offset(skip).limit(limit).all()


def create_user(session: Session, user: schema.CreateUser, user_id: int):
    fake_hashed_password = user.password + "hotreallyhashed"

    user = model.User(email=user.email, hashed_password=fake_hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_items(session: Session, skip: int = 0, limit: int = 100):
    return session.query(model.Item).offset(skip).limit(limit).all()


def create_user_item(session: Session, item: schema.CreateItem, user_id: int):
    item = model.Item(**item.dict(), owner_id=user_id)

    session.add(item)
    session.commit()
    session.refresh(item)

    return item
