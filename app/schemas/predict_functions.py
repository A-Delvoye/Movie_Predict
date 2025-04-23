import pickle as pkl
import pandas as pd
import os
import numpy as np
from app.config import PATH_MODEL_WEIGHT, PATH_OUTPUT_CSV_SCRAPING

def load_model(model_path):
    print("LOAD MODEL")
    with open(model_path, 'rb') as f:
        bundle = pkl.load(f)
        print("LOADED")
    return bundle


def load_weekly_scraping(data_path):
    file = os.listdir(data_path)
    if not file:
        raise FileNotFoundError("Aucun fichier de scraping trouvé !")
    csv_file = [f for f in file if f.endswith('.csv')][0]
    print(50*'*')
    print("CSV_FILE: ", os.path.join(csv_file))
    print(data_path)
    df = pd.read_csv(data_path + '/' + os.path.join(csv_file))
    return df


def data_cleaning(df, columns):
    df['predictions'] = 0
    # df['critics_rating'] = df['critics_rating'].str.replace(',', '.', regex=False)
    # df['critics_rating'] = pd.to_numeric(df['critics_rating'], errors='coerce').fillna(3)
    df['duration'] = df['duration'].fillna(102)

    # Ajout de colonnes manquantes
    for col in columns:
        if col not in df.columns:
            df[col] = 0

    # Encodage des colonnes catégorielles
    df = encode_categories(df, columns)
    df = encode_release_dates(df, columns)
    df = encode_countries(df, columns)
    df = encode_casting(df, columns)

    # Features sur la durée
    df['shortfilm'] = df['duration'].apply(lambda x: x if x < 80 else 0)
    df['medfilm'] = df['duration'].apply(lambda x: x if 80 <= x <= 130 else 0)
    df['longfilm'] = df['duration'].apply(lambda x: x if 130 < x <= 160 else 0)
    df['verylongfilm'] = df['duration'].apply(lambda x: x if x > 160 else 0)

    return df


def encode_categories(df, columns):
    for i, cat in enumerate(df['categories']):
        if isinstance(cat, str):
            for c in cat.split(','):
                if c in columns:
                    df.at[i, c] = 1
    return df


def encode_release_dates(df, columns):
    for i, date in enumerate(df['release_date']):
        if isinstance(date, str):
            parts = date.split(' ')
            if len(parts) >= 3:
                if parts[2] in columns:
                    df.at[i, parts[2]] = 1
                if parts[1] in columns:
                    df.at[i, parts[1]] = 1
    return df


def encode_countries(df, columns):
    for i, country in enumerate(df['country']):
        if isinstance(country, str):
            for c in country.split(','):
                if c in columns:
                    df.at[i, c] = 1
    return df


def encode_casting(df, columns):
    for i, cast in enumerate(df['casting']):
        if isinstance(cast, str):
            for actor in cast.split(','):
                if actor in columns:
                    df.at[i, actor] = 1
    return df


def predict(model,df,columns,csv_columns):
    pred_df = df[csv_columns]
    pred_df['prediction'] = np.round(model.predict(df[columns])/14000).astype(int)
    pred_df = pred_df[pred_df['year']>2023]
    pred_df = pred_df.sort_values('prediction',ascending=False).head(10)
    return pred_df


def start_prediction():
    bundle = load_model(str(PATH_MODEL_WEIGHT))
    columns = bundle['features']
    model = bundle['model']
    data = load_weekly_scraping(str(PATH_OUTPUT_CSV_SCRAPING))
    csv_columns = data.columns
    cleaned_data = data_cleaning(data, columns)
    result = predict(model,cleaned_data,columns, csv_columns)
    return result#(model,cleaned_data,columns, csv_columns)


if __name__ =="__main__":
    # pour tester avec python -m app.schemas.predict_functions
    print(start_prediction())

