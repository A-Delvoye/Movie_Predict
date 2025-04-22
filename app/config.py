from pathlib import Path

# Récupérer le chemin absolu du répertoire racine du projet (Movie_Predict)
BASE_DIR = Path(__file__).resolve().parent.parent

# Définir le chemin relatif du modèle
PATH_MODEL_WEIGHT = BASE_DIR / 'app/data/model_bundle_final.pkl'

PATH_OUTPUT_CSV_SCRAPING = BASE_DIR / 'app/data'