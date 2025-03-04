def userSchema(user) -> dict: 
    """
    Trả về dữ liệu người dùng dưới dạng Object: {}
    """
    return {
        "id": str(user["_id"]), 
        "name": user["name"],
        "age": user["age"],
        "email": user["email"],
        "phone": user["phone"],
        "password": user["password"],
        "avatar": user.get("avatar")
    }

def listUser(users) -> dict:
    return [userSchema(user) for user in users]