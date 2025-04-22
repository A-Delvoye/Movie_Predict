# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlmodel import Session, select
# from app.models.user import User
# from app.schemas.user import UserRead
# from app.db.session import get_session
# from jose import JWTError, jwt
# from app.utils.jwt_handler import verify_token

# router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

# @router.get("/users/me", response_model=UserRead)
# def read_users_me(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
#     payload = verify_token(token)
#     if payload is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token d'authentification invalide",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     username: str = payload.get("sub")

#     statement = select(User).where(User.username == username)
#     user = session.exec(statement).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="L'utilisateur a été supprimé, token invalide")
#     return user


# SECRET_KEY = "your-secret-key"
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 


# def decode_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise JWTError()
#         return {"id": user_id, "username": payload.get("username")}
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token: missing username")
#     except JWTError:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     statement = select(User).where(User.username == username)
#     user = session.exec(statement).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

from fastapi import FastAPI, APIRouter, HTTPException, Depends
from app.models.user import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlmodel import select
from app.db.session import get_session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/admin/users")
async def register_user(name: str, email: str, password: str, role: str, db: Session = Depends(get_session)):

    statement = select(User).where(User.email == email)
    existing_user = db.execute(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password, role=role, activation=False)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully", "user": new_user}