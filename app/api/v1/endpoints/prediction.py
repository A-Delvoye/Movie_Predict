from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.predict_functions import start_prediction
from app.api.v1.endpoints.users import get_current_user
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///./app.db")  # or your real DB

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/predict", response_model=dict)
async def predict(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    pred_df = start_prediction()
    return pred_df
