from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.predict_functions import start_prediction
from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_session
from sqlmodel import Session
import numpy as np

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/predict")
#need to add security feature, anyone can make a prediction
async def predict():
    pred_df = start_prediction()
    pred_df = pred_df.replace([np.nan, np.inf, -np.inf], None)
    return JSONResponse(content={"predictions": pred_df.to_dict(orient="records")})

