from typing import List
from dependencies.auth import CXT, get_current_user
from dependencies.database import Session, select, get_session
from models import UserBase, User, UserCreate, UserInfo, ResetPwd
from fastapi import APIRouter, status, HTTPException, Depends, Query


router = APIRouter(prefix="/user", tags=["Users"], dependencies=[Depends(get_current_user)])


@router.get("/profile", response_model=UserInfo)
async def get_profile(user: User = Depends(get_current_user)):

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid User")

    return user


@router.post("/", response_model=UserInfo)
async def create_user(
    request: UserCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):

    user = User.from_orm(request)

    user.password = CXT.hash(user.password)

    setattr(user, "creator", current_user.id)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/{id}", response_model=UserInfo)
async def get_user(id: int, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    return user


@router.get("/", response_model=List[UserInfo])
async def get_users(
    offset: int = Query(default=0, ge=0), limit: int = Query(default=10, ge=0), session: Session = Depends(get_session)
):

    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.patch("/{id}", response_model=UserInfo)
async def update_user(id: int, request: UserBase, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    for k, v in request.dict().items():
        setattr(user, k, v)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.patch("/{id}/password/reset")
async def reset_password(id: int, request: ResetPwd, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    request.password = CXT.hash(request.password)

    setattr(user, "password", request.password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"detail": "success"}


@router.delete("/{id}")
async def delete_user(id: int, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    session.delete(user)
    session.commit()

    return {"detail": "success"}
