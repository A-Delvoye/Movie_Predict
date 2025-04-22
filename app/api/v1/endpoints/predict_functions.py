import cloudpickle as pkl
import pandas as pd
import os

def load_model(model_path):
    with open(model_path, 'rb') as f:
        bundle = pkl.load(f)
    return bundle['features']

def load_weekly_scraping(data_path):
    file = os.listdir(data_path)
    if not file:
        raise FileNotFoundError("Aucun fichier de scraping trouvé !")
    csv_file = [f for f in file if f.endswith('.csv')][0]
    print(50*'*')
    print(os.path.join(csv_file))
    print(data_path)
    df = pd.read_csv(data_path + '/' + os.path.join(csv_file))
    return df

def data_cleaning(df, columns):
    df['predictions'] = 0
    # Nettoyage des colonnes numériques
    df['critics_rating'] = df['critics_rating'].str.replace(',', '.', regex=False)
    df['critics_rating'] = pd.to_numeric(df['critics_rating'], errors='coerce').fillna(3)
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


def predict(model,df,columns):
    return model.predict(df[columns])



model_file = load_model('/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data/model_bundle_final.pkl')
columns = model_file[1]
model = model_file[0]

data = load_weekly_scraping("/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data")
print(50*'*')
print('DATA')
print(data)

cleaned_data = data_cleaning(data, columns)
print(50*'*')
print('CLEANED_DATA')
print(cleaned_data)


result = predict(model,data,columns)
print(50*'*')
print('RESULT')
print(result)


# with open('/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data/model_bundle_final.pkl', 'rb') as f:
#     bundle = pkl.load(f)
#     model = bundle['model']
#     columns = bundle['features']
# print(50*'*')
# print(columns)
# path = "/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data"
# test = os.listdir(path)
# weekly_scrapy = os.listdir(path)[0]
# # print(50*'*')
# # print(path)
# # print(weekly_scrapy)
# movies_pred = pd.read_csv(path+'/'+weekly_scrapy)
# movies_pred_list = movies_pred.copy()
# movies_pred_list['predictions'] = 0

# movies_pred['critics_rating'] = movies_pred['critics_rating'].str.replace(',', '.')
# movies_pred['critics_rating'] = pd.to_numeric(movies_pred['critics_rating'], errors='coerce')
# movies_pred['critics_rating'][movies_pred['critics_rating'].isna()] = 3
# movies_pred['duration'][movies_pred['duration'].isnull()] = 102

# for col in columns:
#     if col not in movies_pred.columns:
#         movies_pred[col] = 0

# i = 0
# for cat in movies_pred['categories'].iloc[:]:
#     test = cat.split(',')
#     for c in test:
#         if c in columns:
#             movies_pred[c].loc[i] = 1
#     i += 1


# i = 0
# for date in movies_pred['release_date'].iloc[:]:
#     if type(date) == str:
#         d = date.split(' ')
#         if d[2] in columns:
#             movies_pred[d[2]].loc[i] = 1
#     i += 1

# i = 0
# for date in movies_pred['release_date'].iloc[:]:
#     if type(date) == str:
#         d = date.split(' ')
#         if d[1] in columns:
#             movies_pred[d[1]].loc[i] = 1
#     i += 1

# i = 0
# for count in movies_pred['country'].iloc[:]:
#     if type(count) == str:
#         test = count.split(',')
#         for c in test:
#             if c in columns:
#                 movies_pred[c].loc[i] = 1
#     i += 1

# i = 0
# for dir in movies_pred['casting'].iloc[:]:
#     if type(dir) != float:
#         test = dir.split(',')
#         for t in test:
#             if t in columns:
#                 movies_pred[t].loc[i] = 1
#     i+=1

# movies_pred['shortfilm']= [x if x < 80 else 0 for x in movies_pred['duration']]
# movies_pred['medfilm']= [x if x >= 80 and x <=130 else 0 for x in movies_pred['duration']]
# movies_pred['longfilm']= [x if x > 130 and x<=160 else 0 for x in movies_pred['duration']]
# movies_pred['verylongfilm']= [x if x > 160 else 0 for x in movies_pred['duration']]
# movies_pred_df = movies_pred[columns]

# y_pred = model.predict(movies_pred_df)
# movies_pred_list['predictions'] = y_pred
# weekly_scrapy = weekly_scrapy.replace('.csv','')
# pred_df = movies_pred_list[(movies_pred_list['release_date']=='2 avril 2025') & (movies_pred_list['production_year']>2023)].sort_values('predictions',ascending=False).head(10)
# print(pred_df)

# final_result = pred_df.to_json()
