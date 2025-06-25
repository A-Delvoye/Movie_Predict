import sqlite3

file_path = '/home/sami/Documents/Movie_Predict/cinema_prediction/db.sqlite3'  
conn = sqlite3.connect(file_path)
cursor = conn.cursor()

# Supprimer les lignes où 'synopsis' est NULL
cursor.execute("DELETE FROM prediction_app_movies WHERE country IS NULL;")

# Valider les modifications dans la base de données
conn.commit()

# Fermer la connexion à la base de données
conn.close()

