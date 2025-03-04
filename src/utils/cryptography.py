import bcrypt

def hash_password(password: str) -> str:
    """
    Mã hóa mật khẩu
    """
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pw.decode('utf-8')  # Store as string

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Giải mã mật khẩu"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
