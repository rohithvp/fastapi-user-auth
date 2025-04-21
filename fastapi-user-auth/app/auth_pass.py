import bcrypt

def hash_password(password : str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plian_password  :str, hash_password: str)->bool:
    return bcrypt.checkpw(plian_password.encode('utf-8'), hash_password.encode('utf-8'))