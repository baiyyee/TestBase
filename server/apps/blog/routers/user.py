from ..database import get_db
from .. import schemas, models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, status, HTTPException


router = APIRouter(prefix="/user", tags=["Users"])


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=schemas.ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):

    request.password = pwd_cxt.hash(request.password)

    new_user = models.User(**request.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.ShowUser, tags=["users"])
def get_user(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not avaliable")
    return user
