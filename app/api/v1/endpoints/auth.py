from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlmodel import select
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.models.user import User
from app.db.session import get_session
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key") 
ALGORITHM = os.getenv("ALGORITHM", "HS256") 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def get_password_hash(password: str) -> str:
    """Hash the password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if a plain password matches its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """Retrieve the currently authenticated user from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        statement = select(User).where(User.email == email)
        result = session.execute(statement).first()
        user = result[0] if result else None
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")



@router.post("/auth/login", summary="Authenticate a user and return an access token")
async def authenticate_user(email: str, password: str, db: Session = Depends(get_session)):
    """Authenticate a user using their email and password."""
    statement = select(User).where(User.email == email)
    result = db.execute(statement).first()
    user = result[0] if result else None
    if not user or not verify_password(password, user.hashed_password):  
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/logout", summary="Log out the user by deleting the access token cookie")
def logout(response: Response):
    """Log out the user by removing the access token cookie."""
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}