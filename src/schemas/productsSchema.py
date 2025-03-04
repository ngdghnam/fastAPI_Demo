def productSchema(product) -> dict: 
    return {
        "id": str(product["_id"]), 
        "name": product["name"],
        # "description": str(product.get("description", "No description available")),
        "description": product.get("description") or product.get("description ") or "No description available",
        "price": product.get("price", 0)
    }

def listProduct(products) -> dict:
    return [productSchema(product) for product in products]