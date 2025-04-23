from django.shortcuts import render, redirect
from .models import Movies
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
from collections import defaultdict
from django.conf import settings
from dotenv import load_dotenv
import sqlite3
import requests
import json
import os

load_dotenv()

API_PREDICTION_URL = "http://127.0.0.1:8001/api/v1/predict"
API_BASE_URL = "http://127.0.0.1:8001"
API_USER_ID = "JeremyCinema"
email = "cinema@films.fr"
password = "cinema"

@login_required
def prediction_view(request):
    headers = {
            "Content-Type": "application/json"}
    payload = {
        "user_id": API_USER_ID  
    }

    try:
    # Envoi de la requête à l'API FastAPI
        response = requests.post(API_PREDICTION_URL, headers=headers, json = payload)
        prediction_data = response.json()
        print(50*'*')
        # print(prediction_data)
        # Exporter dans le répertoire courant
        file_path = os.path.join(os.getcwd(), 'prediction_app/prediction_result.json')
        with open(file_path, 'w') as f:
            json.dump(prediction_data, f, indent=4)

        print(f"Fichier JSON sauvegardé à : {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
        prediction_data = {"error": "Impossible de récupérer les données de prédiction."}
# Vérifier la réponse de l'API
    return render(request, "predictions.html", {
        "prediction_data": prediction_data
    }) 


# @login_required
# def prediction_view(request):
#     predictions = []
#     if request.method == 'POST':

#         file_path = settings.BASE_DIR / 'db.sqlite3'
#         conn = sqlite3.connect(file_path)

#         query = "SELECT DISTINCT title, prediction, image_url, synospis, casting FROM prediction_app_movies"

#         df = pd.read_sql_query(query, conn)
#         conn.close()

#         for _, row in df.iterrows():
#             prediction, created = Movies.objects.get_or_create(
#                 # user=request.user,
#                 title=row['title'],
#                 prediction=row['prediction'],
#                 casting = row['casting'],
#                 image_url=row['image_url'],
#                 synospis=row['synospis'],
                
#             )
#             predictions.append(prediction)
#     predictions_sorted = sorted(predictions, key=lambda x: x.prediction, reverse=True)
#     return render(request, 'predictions.html', {'predictions': predictions_sorted})


@login_required
def history_view(request):
    # predictions = Movies.objects.filter(user=request.user).order_by('-date')
    predictions = Movies.objects.order_by('-release_date')
    # Grouper par semaine (année + n° de semaine)
    grouped_predictions = defaultdict(list)

    for p in predictions:
        year, week, _ = p.release_date.isocalendar()  # isocalendar() → (année, semaine, jour)
        grouped_predictions[f"Semaine {week} - {year}"].append(p)

    # Trier les groupes par semaine descendante
    grouped_predictions = dict(sorted(grouped_predictions.items(), reverse=True))

    return render(request, 'prediction_app/history.html', {
        'grouped_predictions': grouped_predictions
    })

