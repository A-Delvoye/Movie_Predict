from sqlmodel import SQLModel, Field
from datetime import datetime

# class PredictionHistory(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     State: str
#     Zip: str
#     BankState: str
#     ApprovalFY: int
#     Term: int
#     NoEmp: int
#     NewExist: int
#     CreateJob: int
#     RetainedJob: int
#     FranchiseCode: int
#     UrbanRural: int
#     RevLineCr: int
#     LowDoc: int
#     DisbursementGross: float
#     GrAppv: float
#     ApprovalMonth: int
#     NAICS_CODE: str
#     prediction: int
#     user_id: int = Field(..., foreign_key="user.id", description="Identifiant de l'utilisateur associé à la prédiction")
#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now)

#     user: Optional["User"] = Relationship(back_populates="predictions")