import json
import time
from fastapi import APIRouter, HTTPException, Depends, responses, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import sqlite3
from datetime import datetime, timedelta

from encryption import decrypt
from jwt_utils import get_auth_details



auth_router = APIRouter()
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@auth_router.post("/register")
def register(user: UserCreate):
    hashed_pw = get_password_hash(user.password)
    try:
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_pw))
        conn.commit()
        return {"message": "User registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already taken")
    finally:
        conn.close()


from encryption import encrypt
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"




@auth_router.post("/login")
def login(username: str, password: str, request: Request):
    print("at login")
    print(f'{username = }')
    print(f'{password = }')
    
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    db_user = cursor.fetchone()
    conn.close()

    if not db_user or not verify_password(password, db_user[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    expires = time.time()+(60*60*24*7)
    access_token = encrypt(json.dumps({"sub": username, "exp": expires}))
    response = responses.JSONResponse(content={"message": "cookie set"})
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,    # Prevent XSS attacks
        secure=True,      # HTTPS only
        samesite='Lax'    # CSRF protection
    )
    return response





@auth_router.get("/name")
def get_name(request: Request) -> str:
    auth_details: str = get_auth_details(request)
    return auth_details
   




@auth_router.get("/me")
def read_current_user(request: Request) -> str:
    auth_details: str = get_auth_details(request)
    return auth_details
    














