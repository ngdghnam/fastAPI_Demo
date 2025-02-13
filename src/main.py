from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Routers/ Controllers
from controllers import user_controller 
from controllers import auth_controller

templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Path to static files 
app.mount("/static", StaticFiles(directory="static"), name="static")

devs = [
    {'fullName': "Nguyen Dang Hoai Nam", 'role': 'Main Dev'},
    {'fullName': "Huynh Ngoc Cuong", 'role': 'Backend Dev'},
    {'fullName': "Duong Thanh Binh", 'role': 'Frontend Dev'},
    {'fullName': "Minh Tuyen", 'role': 'Designer'},
    {'fullName': "Vi Do", 'role': 'Designer'},
    {'fullName': "Le Minh Nguyen", 'role': 'Team Leader'},
]

# Using templates 
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "message": "This is AI4I's Website",
        "devs": devs
    })


app.include_router(user_controller.router)
app.include_router(auth_controller.router)
