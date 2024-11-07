from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#PASSWORD 
def get_password_has(password: str) -> str:
    return pwd_context.hash(password)

#PASSWORD
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

