from . import models
from fastapi import FastAPI
from .database import engine
from .routers import auth, blog, user


models.Base.metadata.create_all(engine)


app = FastAPI()


app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)
