from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from validates.user_validate import validate_user_input
from models.user import User

# Initialize Jinja templates
templates = Jinja2Templates(directory="templates")

# Create router
router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/", response_class=HTMLResponse)
def getUserView(request: Request): 
    users = User.all()
    return templates.TemplateResponse("user/index.html", {
        "request": request, 
        "message": "This is Hoai Nam from AI4I club",
        "users": users
    })

@router.get("/create", response_class=HTMLResponse)
async def getCreateView(request: Request): 
    return templates.TemplateResponse("/user/create.html", {
        "request": request, 
    })

@router.post("/create", response_class=HTMLResponse)
async def createUser(
    request: Request,
    validated_data: dict = Depends(validate_user_input)
):
    try:
        if "errors" in validated_data:
            return templates.TemplateResponse(
                "user/create.html",
                {"request": request, **validated_data}
            )

        # Hash password before saving
        hashed_password = User.hashPassword(validated_data["password"])

        # Create and save user
        new_user = User.create(
            name=validated_data["name"], 
            phone=validated_data["phone"], 
            email=validated_data["email"], 
            password=hashed_password            
        )
        new_user.save()
        
        # Redirect to user list
        return RedirectResponse(url="/user", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
