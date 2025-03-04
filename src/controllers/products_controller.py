from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import ReturnDocument
from models.products import Products
from config.database import productCollection
from schemas.productsSchema import listProduct
from bson import ObjectId

# templates
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", response_class=HTMLResponse)
async def getProducts(req: Request, page: int = Query(1, ge=1)):
    # pagination 
    # pagination 
    perPage = 10
    skip = (page - 1) * perPage
    

    # products = listProduct(productCollection.find())
    # product_cursor = productCollection.find()  
    # products_list = await product_cursor.to_list(None)  # Convert cursor to a list
    # products = listProduct(products_list)  # Now pass a proper list

    product_cursor = productCollection.find().skip(skip).limit(perPage)
    products_list = await product_cursor.to_list(length=perPage)  # Convert cursor to a list
    products = listProduct(products_list)  # Now pass a proper list

    # print(products_list)

    return templates.TemplateResponse("product/index.html", {
        "request": req, 
        "products": products,
        "page": page,
        "perPage": perPage
    })

@router.get("/{id}")
async def getProductById(id: str):
    try:
        # Ensure the ID is a valid ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        # Find product by ID
        product = await productCollection.find_one({"_id": ObjectId(id)})

        # Check if product exists
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Convert ObjectId to string for JSON serialization
        product["_id"] = str(product["_id"])

        return {
            "message": "Product found successfully",
            "product": product
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.post("/create-product", status_code=201)
async def postProduct(product: Products):
    try:
        await productCollection.insert_one(dict(product))
        return {
            "message": "Create new product successfully", 
            "status": f'{201}', 
            "productName": product.name
        }
    except Exception as e: 
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@router.put("/update-product/{id}")
async def putProduct(id: str, product: Products):
    try:
        # Validate the ID format
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        # Convert product model to dictionary
        product_dict = product.model_dump()  # For Pydantic v2 (use dict(product) for Pydantic v1)

        # Perform the update
        updatedProduct = await productCollection.find_one_and_update(
            {"_id": ObjectId(id)},  # Correct: Use ObjectId directly
            {"$set": product_dict},
            return_document=ReturnDocument.AFTER  # Returns the updated document
        )

        # Check if a product was actually updated
        if updatedProduct is None:
            raise HTTPException(status_code=404, detail="Product not found or no update was made")

        # Convert `_id` to string before returning
        updatedProduct["_id"] = str(updatedProduct["_id"])

        return {
            "message": "Update completed successfully",
            "updated_product": updatedProduct
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/{id}")
async def deleteProduct(id: str):
    try:
        # Ensure the ID is a valid ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")

        # Attempt to delete the product
        deleted_product = await productCollection.find_one_and_delete({"_id": ObjectId(id)})

        # If no product was deleted, return a 404 response
        if deleted_product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"message": "Deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")