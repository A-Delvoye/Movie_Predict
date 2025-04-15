from django.shortcuts import render, redirect
from .models import Movies
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
from collections import defaultdict
from django.conf import settings
import os
import csv


# def home(request):
#     return render(request, 'home.html')


@login_required
def prediction_view(request):
    predictions = []
    if request.method == 'POST':
        # Lire les prédictions depuis un fichier CSV
        # file_path = os.path.join(settings.BASE_DIR, 'weekly_predict.csv')
        file_path = settings.BASE_DIR / 'prediction_app' / 'weekly_predict.csv'
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            prediction = Movies.objects.create(
                # user=request.user,
                title=row['title'],
                url_image=row['image_url'],
                release_date = row['release_date'],
                prediction=row['places_predites'],
                
            )
            predictions.append(prediction)
    predictions_sorted = sorted(predictions, key=lambda x: x.prediction, reverse=True)
    return render(request, 'predictions.html', {'predictions': predictions_sorted})

# def predict_view(request):
#     predictions = []
#     if request.method == 'POST':
#         # Lire les prédictions depuis un fichier CSV
#         file_path = os.path.join(settings.BASE_DIR, 'weekly_predict.csv')
#         df = pd.read_csv(file_path)

#         for _, row in df.iterrows():
#             prediction = Movies.objects.create(
#                 user=request.user,
#                 title=row['title'],
#                 release_date=datetime.now().date(),  # Ou extraire d'un champ si dispo
#                 prediction_score=row['places_predites']
#             )
#             predictions.append(prediction)

#     return render(request, 'predictions.html', {'predictions': predictions})





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


# @login_required
# def history_view(request):
#     predictions = Movies.objects.filter(user=request.user).order_by('-date')
#     return render(request, 'history.html', {'predictions': predictions})