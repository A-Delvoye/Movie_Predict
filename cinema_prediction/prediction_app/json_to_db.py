import pandas as pd
import sqlite3
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
print('BASE_DIR JSON2DB')
print('base_dir :', base_dir)
# Chemins relatifs
# json_path = base_dir / 'prediction_app' / 'prediction_result.json'
json_path = base_dir / 'prediction_app' / 'weekly.json'

print('json_path :',json_path)
db_path = base_dir / 'db.sqlite3'
print('db_path :', db_path)

# json_path = 'prediction_result.json'

df = pd.read_json(json_path)

# Convertir les colonnes contenant des dict ou des listes en chaînes
for col in df.columns:
    if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
        print(f"Conversion de la colonne '{col}' en chaîne de caractères")
        df[col] = df[col].apply(lambda x: str(x))

    
# db_path = 'db.sqlite3'
conn = sqlite3.connect(db_path)

table_name = 'prediction_app_movies'

df.to_sql(table_name, conn, if_exists='replace', index=False)

conn.close()

