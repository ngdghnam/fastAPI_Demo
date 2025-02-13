from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Initialize Jinja templates
templates = Jinja2Templates(directory="templates")

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/", response_class=HTMLResponse)
def getUserView(request: Request): 
    return templates.TemplateResponse("auth/login.html", {
        "request": request, 
    })