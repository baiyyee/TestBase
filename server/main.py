from models import User
from dependencies.auth import CXT
from routers import auth, user, file
from jose import ExpiredSignatureError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from dependencies.database import SQLModel, Session, engine
from sqlalchemy.exc import IntegrityError as SqlAlchemyIntegrityError
from starlette.exceptions import HTTPException as StarletteHTTPException


description = "API Demo Is Used For API Testing. 🚀"

app = FastAPI(
    docs_url="/",
    title="API Demo",
    description=description,
    version="0.0.1",
    contact={
        "name": "Huabo He",
        "url": "https://baiyyee.github.io/",
        "email": "hhbstar@hotmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
)


@app.exception_handler(ExpiredSignatureError)
async def sqlalchemy_exception_handler(request, exc):

    return JSONResponse(content={"error": str(exc)}, status_code=status.HTTP_401_UNAUTHORIZED)


@app.exception_handler(SqlAlchemyIntegrityError)
async def sqlalchemy_exception_handler(request, exc):

    message = {error.split(".")[-1]: error.split(":")[0] for error in exc.args}
    return JSONResponse(content={"error": message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):

    return JSONResponse(content={"error": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    message = {error.get("loc")[-1]: error.get("msg") for error in exc.errors()}
    return JSONResponse(content={"error": message}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.on_event("startup")
async def init_db():

    # Clean Up DB Table
    SQLModel.metadata.drop_all(engine)

    # Init DB Table
    SQLModel.metadata.create_all(engine)

    # Init User
    with Session(engine) as session:
        user = User(name="root", email="root@test.com", role=0, status=1, creator=1)
        user.password = CXT.hash("123456")
        session.add(user)
        session.commit()


# @app.on_event("shutdown")
# async def clean_db():

#     # Clean Up DB Table
#     SQLModel.metadata.drop_all(engine)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(file.router)


# cd OneStep/server
# uvicorn main:app --reload --debug

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True, debug=True)
