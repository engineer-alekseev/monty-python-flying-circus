import uvicorn
from fastapi.responses import HTMLResponse

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# from app_auth.view import app_auth
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)

@app.get("/user", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("user.html", context)

@app.get("/content", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("content.html", context)


@app.get("/drop", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("drop.html", context)



@app.get("/admin", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("admin.html", context)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
