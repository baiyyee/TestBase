from models import User
from dependencies.auth import CXT
from routers import auth, user, file
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dependencies.database import engine, SQLModel, Session
from starlette.exceptions import HTTPException as StarletteHTTPException


description = "API Demo Is Used For API Testing. 🚀"

app = FastAPI(docs_url="/", title="API Demo", description=description, version="0.0.1")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):

    return JSONResponse({"message": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    error_message = {}
    for error in exc.errors():
        field = error.get("loc")[-1]
        error_message[field] = [{"code": error.get("type"), "message": error.get("msg")}]

    return JSONResponse({"message": "Field Invalid", "fields": error_message})


@app.on_event("startup")
async def init_db():

    # Init DB Table
    SQLModel.metadata.create_all(engine)

    # Init User
    with Session(engine) as session:
        user = User(name="root", email="root@test.com", role=0, status=1, password=CXT.hash("123456"), creator=1)
        session.add(user)
        session.commit()


@app.on_event("shutdown")
async def clean_db():

    # Clean Up DB Table
    SQLModel.metadata.drop_all(engine)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(file.router)


# cd OneStep/server
# uvicorn main:app --reload --debug

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8080, reload=True, debug=True)
