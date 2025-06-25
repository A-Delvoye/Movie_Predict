from app.db.session import engine
from app.models.user import User 
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
