from bson import ObjectId
from fastapi import APIRouter, Form, HTTPException, Request, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

import uuid

from config.database import userCollection, fs
from schemas.usersSchema import listUser

from validates.user_validate import validate_user_form

from utils.cryptography import hash_password

# templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_class=HTMLResponse)
async def getUsers(req: Request):
    users_cursor = userCollection.find()  
    users_list = await users_cursor.to_list(None)  # Convert cursor to a list
    users = listUser(users_list)  # Now pass a proper list

    return templates.TemplateResponse("user/index.html", {
        "request": req,
        "users": users 
    })

@router.get("/create", response_class=HTMLResponse)
async def renderCreateTemplate(req: Request):
    return templates.TemplateResponse("user/create.html", {
        "request": req
    })

@router.post("/create", response_class=HTMLResponse)
async def createUser(
    request: Request, 
    name: str = Form(...),
    age: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(...)
):
    try:
        age_int = None
        if age.strip():
            try:
                age_int = int(age)
            except ValueError:
                return templates.TemplateResponse(
                    "user/create.html", 
                    {"request": request, "errors": ["Age must be a valid number"]}
                )

        errors = validate_user_form(name, age_int, email, phone, password, avatar)

        if errors: 
            return templates.TemplateResponse("user/create.html", {"request": request, "errors": errors})

        # Check for existing user
        existing_user = await userCollection.find_one({"email": email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Handle avatar upload
        avatar_id = None
        if avatar and avatar.filename:
            contents = await avatar.read()
            unique_filename = f"{uuid.uuid4()}.jpg"

            # Use async GridFS to store file
            avatar_id = await fs.upload_from_stream(
                unique_filename, 
                contents, 
                metadata={"content_type": avatar.content_type} 
            )

        # Hash password
        hashedPassword = hash_password(password)

        # Create new user document
        newUser = {
            "name": name,
            "age": age,
            "phone": phone,
            "email": email,
            "password": hashedPassword,
            "avatar": str(avatar_id) if avatar_id else None,
        }
        
        # Insert user into database using async client
        result = await userCollection.insert_one(newUser)

        if not result.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to create user")
            
        return RedirectResponse(url="/users", status_code=303)
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/avatar/{avatar_id}")
async def get_avatar(avatar_id: str):
    try:
        file_id = ObjectId(avatar_id)
        grid_out = await fs.open_download_stream(file_id)
        return StreamingResponse(grid_out, media_type="image/jpeg")
    except Exception:
        raise HTTPException(status_code=404, detail="Image not found")