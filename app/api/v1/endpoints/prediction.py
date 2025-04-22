import os
import pickle
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
import xgboost

router = APIRouter()
with open("app/data/model_bundle2.pkl", "rb") as f:
    model = pickle.load(f)
print("✅ Modèle chargé avec succès")



@router.post("/predict", response_model=dict)
async def predict(data: LoanApplication, db: Session = Depends(get_db), user_id: int = Depends(get_db)):
    """Endpoint pour prédire l'approbation d'un prêt sans token"""








# print(model)
    # Extraction des features



# def login():
#     username = os.getenv("API_USERNAME")
#     password = os.getenv("API_PASSWORD")

#     if not username or password:
#         raise Exception("Please set API_USERNAME and API_PASSWORD in your .env file")
    
#     login_data = {
#         "username" : username,
#         "password" : password,
#     }

#     response = request.post(f"{BASE_URL}/api/v1/login",json=login_data)
#     if response.status_code ==200:
#         token = response.json()["access_token"]
#         set_key(ENV_FILE, "API_TOKEN", token)
#         return token
#     else:
#         raise Exception("Failed to login")
    
# def make_prediction(data:dict):
#     token = os.getenv("API_TOKEN")
#     headers = {
#         "Authorization" : f"Bearer {token}"}
    
#     response = request.post(
#         f"{BASE_URL}/api/v1/predict",
#         json = data,
#         headers = headers
#     )

#     if response.status_code ==200:
#         return response.json()
    
#     elif response.status_code == 401:
#         new_token = login()
#         headers = {"Authorization" : f"Bearer{new_token}"}
#         response = request.post(f"{BASE_URL}/api/v1/predict",
#                                 json = data,
#                                 headers = headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise Exception("login or password incorrect")
        
#     else:
#         raise Exception("Failed to make a prediction")
    
# def main():
#     data = {
#         ""
#     }

#     response = make_prediction(data)
#     print(response)





# OLD PROJECT

# router = APIRouter()
# with open("app/data/catboost_best_grid_model.pkl", "rb") as f:
#     model = pickle.load(f)
# print("✅ Modèle chargé avec succès")

# @router.post("/predict", response_model=dict)
# async def predict(data: LoanApplication, db: Session = Depends(get_db), user_id: int = Depends(get_db)):
#     """Endpoint pour prédire l'approbation d'un prêt sans token"""
    
#     # Vérifier si l'utilisateur existe
#     user = db.exec(select(User).where(User.id == user_id)).first()
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")

#     # Extraction des features
#     feature = [[
#         data.State, data.Zip, data.BankState, data.ApprovalFY, data.Term,
#         data.NoEmp, data.NewExist, data.CreateJob, data.RetainedJob,
#         data.FranchiseCode, data.UrbanRural, data.RevLineCr, data.LowDoc,
#         data.DisbursementGross, data.GrAppv, data.ApprovalMonth, data.NAICS_CODE,
#     ]]

#     # Prédiction
#     resultat = model.predict(feature)
#     prediction_result = int(resultat[0])

#     # Enregistrement en base de données
#     new_prediction = PredictionHistory(
#         **data.dict(),
#         prediction=prediction_result,
#         user_id=user.id,
#         created_at=datetime.now(),
#         updated_at=datetime.now()
#     )
#     db.add(new_prediction)
#     db.commit()
#     db.refresh(new_prediction)

#     return {"prediction": prediction_result}
