from fastapi import FastAPI
from users.views import user_router, token_router
from content.views import content_router
from tags.views import tags_router
from fastapi.middleware.cors import CORSMiddleware
from database_handler import database
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from users.services import authenticate_user
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="/home/bytecode/projects/monty-python-flying-circus-actual/templates/")
app.mount("/static", StaticFiles(directory="/home/bytecode/projects/monty-python-flying-circus-actual/static/", html=True), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)

@app.post("/", response_class=HTMLResponse)
async def login_get(request: Request):
    s = await request.body()
    log = s.decode("utf-8").split("&")
    login = log[0].split('=')[1]
    password = log[1].split('=')[1]
    # print(login,password)
    user = await authenticate_user(login, password)
    context = {
        "request": request,
    }
    if not user:
        return templates.TemplateResponse("content.html", context)
    return templates.TemplateResponse("content.html", context)


@app.get("/content", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("content.html", context)


@app.get("/static/<path>", response_class=HTMLResponse)
def stat(path:str,request: Request):
    return templates.TemplateResponse(path, context)
    
app.include_router(user_router)
app.include_router(token_router)
app.include_router(content_router)
app.include_router(tags_router)


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)