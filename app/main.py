from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
# from app.schemas import 
from contextlib import asynccontextmanager
from app.api.v1.endpoints import auth, users, prediction
from app.db.session import engine
from sqlmodel import SQLModel

app = FastAPI(title="Movie Predict API",
              description= "API pour prédire l'affluence des films de la semaine")

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(users.router, prefix="/api/v1", tags=["prediction"])


@app.get("/")
def home():
    """Return a welcome message for the API's root endpoint.

    This endpoint serves as a simple health check and provides a welcome message.
    """
    return {"message": "APIBanque - Bienvenue sur l'API de prédiction de films"}



# @app.post("/predict", response_model=FilmPredictionResponse)
# async def predict_affluence(films: List[FilmInput]):
#     """
#     Prédit l'affluence pour une liste de films.
    
#     Chaque film est spécifié avec ses métadonnées comme les acteurs, réalisateurs, etc.
#     """
#     try:
#         results = []
#         for film in films:
#             prediction = predict_film_affluence(film)
#             results.append({
#                 "title": film.title if hasattr(film, "title") else "Unknown",
#                 "predicted_affluence": prediction
#             })
        
#         return {"predictions": results}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
