from typing import List
from sqlalchemy.orm import Session
from . import schema, service, model
from .database import SessionLocal, engine
from fastapi import Depends, APIRouter, HTTPException


model.Base.metadata.create_all(bind=engine)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=schema.User)
def create_user(user: schema.CreateUser, session: Session = Depends(get_db)):
    user = service.get_user_by_email(session, email=user.email)

    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(session, user)


@router.get("/users/", response_model=List[schema.User])
def get_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    users = service.get_users(session, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schema.User)
def get_user(user_id: int, session: Session = Depends(get_db)):
    user = service.get_user(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/items/", response_model=schema.Item)
def create_item_for_user(user_id: int, item: schema.CreateItem, session: Session = Depends(get_db)):
    return service.get_items(session, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schema.Item])
def get_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    return service.get_items(session, skip=skip, limit=limit)


# @router.get("/")
# async def index():
#     return {"name": testdata.name(), "age": testdata.int(18, 35), "gender": testdata.gender()}


# @router.get("/person/{id}")
# async def get_person(id: int, q: Union[str, None] = None):
#     return {"id": id, "name": testdata.name(), "age": testdata.int(18, 35), "gender": testdata.gender(), "q": q}


# @router.put("/person/{id}")
# async def update_person(id: int, person: Person):
#     return {"id": id, "name": person.name, "age": person.age, "gender": person.gender}


# @router.post("/files/")
# async def create_files(files: List[bytes] = File()):
#     return {"file_sizes": [len(file) for file in files]}


# @router.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}


# @router.get("/upload")
# async def upload():
#     content = """
#         <body>
#         <form action="/files/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#         </form>
#         <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
#         <input name="files" type="file" multiple>
#         <input type="submit">
#         </form>
#         </body>
#     """
#     return HTMLResponse(content=content)
