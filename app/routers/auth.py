from models import User
from datetime import timedelta
from const import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.auth import CXT, create_access_token
from dependencies.database import Session, engine, select
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(tags=["Authorization"])


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends()):

    with Session(engine) as session:

        user = session.exec(select(User).where(User.email == request.username)).first()

        if (not user) or (not CXT.verify(request.password, user.password)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email, "scopes": request.scopes}, expires_delta=access_token_expires)

        return {"token_type": "bearer", "access_token": access_token}
