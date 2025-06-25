from fastapi import FastAPI, HTTPException
from typing import List
import uvicorn
from contextlib import asynccontextmanager
from app.api.v1.endpoints import auth, users, prediction
from app.db.session import engine
from sqlmodel import SQLModel

app = FastAPI(title="Movie Predict API",
              description= "API pour prédire l'affluence des films de la semaine")

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])


@app.get("/")
def home():
    """Return a welcome message for the API's root endpoint.

    This endpoint serves as a simple health check and provides a welcome message.
    """
    return {"message": "APIBanque - Bienvenue sur l'API de prédiction de films"}
