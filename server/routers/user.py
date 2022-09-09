from typing import List
from dependencies.auth import CXT, get_current_user
from fastapi import APIRouter, Depends, status, HTTPException
from dependencies.database import Session, select, get_session
from models import UserBase, User, UserCreate, UserInfo, ResetPwd


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

    request.password = CXT.hash(request.password)

    user = User.from_orm(request)

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
async def get_users(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):

    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.put("/{id}", response_model=UserInfo)
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


@router.patch("/{id}/password/reset", response_model=UserInfo)
async def reset_password(id: int, request: ResetPwd, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    request.password = CXT.hash(request.password)

    setattr(user, "password", request.password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, session: Session = Depends(get_session)):

    user = session.get(User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User ID {id}")

    session.delete(user)
    session.commit()

    return {"detail": "success"}
