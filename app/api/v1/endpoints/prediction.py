from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from Movie_Predict.app.schemas.predict_functions import start_prediction

router = APIRouter()


@router.post("/predict", response_model=dict)
async def predict(db: Session = Depends(get_db), user_id: int = Depends(get_db)):
    pred_df = start_prediction()
    return pred_df
