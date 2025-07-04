from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.predict_functions import start_prediction
from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_session
from sqlmodel import Session
from app.models.user import User
import numpy as np
import pandas as pd

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/predict")
# async def predict(current_user: User = Depends(get_current_user)):
async def predict():
    print(50*'#')
    pred_df = start_prediction()
    pred_df = pred_df.replace([np.nan, np.inf, -np.inf], None)
    return JSONResponse(content={"predictions": pred_df.to_dict(orient="records")})
    # return JSONResponse(content={pred_df.to_dict(orient="records")})

# @router.get("/top10")
# def get_predictions():
#     df = pd.read_csv("fichier_prediction.csv")
#     return JSONResponse(content=df.to_dict(orient="records"))
