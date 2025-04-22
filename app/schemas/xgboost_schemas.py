# from pydantic import BaseModel, Field
from typing import Optional
import pickle
import xgboost 

with open("app/data/model_bundle.pkl", "rb") as f:
    model = pickle.load(f)
print("✅ Modèle chargé avec succès")

# try:
#     if hasattr(model, 'feature_names_in_'):
#         columns = model.feature_names_in_
#     elif hasattr(model, 'preprocessor') and hasattr(model.preprocessor, 'feature_names_in_'):
#         columns = model.preprocessor.feature_names_in_
#     else:
#         raise AttributeError("Impossible de trouver les colonnes d'entrée.")
    
#     print("✅ Colonnes détectées :", columns)

# except Exception as e:
#     print("❌ Erreur pour récupérer les colonnes :", e)

feature_names = model.get_booster().feature_names
print(feature_names)