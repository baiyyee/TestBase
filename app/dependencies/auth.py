from jose import jwt
from .. import const
from typing import Union
from ..models import User
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from ..dependencies.database import Session, get_session, select


CXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=10)

    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, const.SECRET_KEY, algorithm=const.ALGORITHM)

    return token


async def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl=const.TOKEN_URL)), session: Session = Depends(get_session)
):

    payload = jwt.decode(token, const.SECRET_KEY, algorithms=[const.ALGORITHM])

    email = payload.get("sub")

    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    user = session.exec(select(User).where(User.email == email)).one_or_none()

    return user
