from functools import lru_cache
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.configuration import Settings

# routers 
from controllers import products_controller
from controllers import users_controller

# templates
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# Path to static files 
app.mount("/static", StaticFiles(directory="static"), name="static") #Link đến folder static

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

# 404 Handler
def not_found_error(request: Request, exc: HTTPException):
    """
    Render ra trang errror_not_found.html
    """
    return templates.TemplateResponse("errror_not_found.html", {
        "request": request,
        "status_code": 404,
        "message": "Oops! The resource you requested was not found."
    }, status_code=404)

@app.exception_handler(404)
def not_found_exception_handler(request: Request, exc: HTTPException):
    """
    Nếu user nhập vào 1 đường link ko tồn tại sẽ trả ra 
    error 404 
    """
    return not_found_error(request, exc)


app.include_router(products_controller.router)
app.include_router(users_controller.router)
