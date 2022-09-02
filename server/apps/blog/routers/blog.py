from typing import List
from ..database import get_db
from .. import schemas, models
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from fastapi import APIRouter, Depends, status, Response, HTTPException


router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@router.get("/", response_model=List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not avaliable")

    return blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} is not avaliable")

    blog.update(request.dict())
    db.commit()

    return {"detail": "success"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_blog(
    id: int, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with the id {id} is not avaliable"}

    blog.delete(synchronize_session=False)
    db.commit()

    return {"detail": "success"}
