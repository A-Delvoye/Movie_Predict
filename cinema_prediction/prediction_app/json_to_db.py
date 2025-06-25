import pandas as pd
import sqlite3

json_path = '/home/sami/Documents/Movie_Predict/cinema_prediction/prediction_app/weekly.json'
#A CHANGER

df = pd.read_json(json_path)

db_path = '/home/sami/Documents/Movie_Predict/cinema_prediction/db.sqlite3'
#A CHANGER

conn = sqlite3.connect(db_path)

table_name = 'prediction_app_movies'

df.to_sql(table_name, conn, if_exists='replace', index=False)

conn.close()

