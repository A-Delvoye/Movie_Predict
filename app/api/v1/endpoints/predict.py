import cloudpickle as pkl
import pandas as pd
import os


with open('/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data/model_bundle_final.pkl', 'rb') as f:
    bundle = pkl.load(f)
    model = bundle['model']
    columns = bundle['features']
print(50*'*')
print(columns)
path = "/home/antoine/Documents/Projets_DEV_IA/Allocine_scraping/FastAPI/Projet_API/Movie_Predict/app/data"
test = os.listdir(path)
weekly_scrapy = os.listdir(path)[0]
# print(50*'*')
# print(path)
# print(weekly_scrapy)
movies_pred = pd.read_csv(path+'/'+weekly_scrapy)
movies_pred_list = movies_pred.copy()
movies_pred_list['predictions'] = 0

movies_pred['critics_rating'] = movies_pred['critics_rating'].str.replace(',', '.')
movies_pred['critics_rating'] = pd.to_numeric(movies_pred['critics_rating'], errors='coerce')
movies_pred['critics_rating'][movies_pred['critics_rating'].isna()] = 3
movies_pred['duration'][movies_pred['duration'].isnull()] = 102

for col in columns:
    if col not in movies_pred.columns:
        movies_pred[col] = 0

i = 0
for cat in movies_pred['categories'].iloc[:]:
    test = cat.split(',')
    for c in test:
        if c in columns:
            movies_pred[c].loc[i] = 1
    i += 1


i = 0
for date in movies_pred['release_date'].iloc[:]:
    if type(date) == str:
        d = date.split(' ')
        if d[2] in columns:
            movies_pred[d[2]].loc[i] = 1
    i += 1

i = 0
for date in movies_pred['release_date'].iloc[:]:
    if type(date) == str:
        d = date.split(' ')
        if d[1] in columns:
            movies_pred[d[1]].loc[i] = 1
    i += 1

i = 0
for count in movies_pred['country'].iloc[:]:
    if type(count) == str:
        test = count.split(',')
        for c in test:
            if c in columns:
                movies_pred[c].loc[i] = 1
    i += 1

i = 0
for dir in movies_pred['casting'].iloc[:]:
    if type(dir) != float:
        test = dir.split(',')
        for t in test:
            if t in columns:
                movies_pred[t].loc[i] = 1
    i+=1

movies_pred['shortfilm']= [x if x < 80 else 0 for x in movies_pred['duration']]
movies_pred['medfilm']= [x if x >= 80 and x <=130 else 0 for x in movies_pred['duration']]
movies_pred['longfilm']= [x if x > 130 and x<=160 else 0 for x in movies_pred['duration']]
movies_pred['verylongfilm']= [x if x > 160 else 0 for x in movies_pred['duration']]
movies_pred_df = movies_pred[columns]

y_pred = model.predict(movies_pred_df)
movies_pred_list['predictions'] = y_pred
weekly_scrapy = weekly_scrapy.replace('.csv','')
pred_df = movies_pred_list[(movies_pred_list['release_date']=='2 avril 2025') & (movies_pred_list['production_year']>2023)].sort_values('predictions',ascending=False).head(10)
print(pred_df)

final_result = pred_df.to_json()
