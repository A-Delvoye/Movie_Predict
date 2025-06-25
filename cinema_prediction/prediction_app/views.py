from django.shortcuts import render, redirect
from .models import Movies
from django.contrib.auth.decorators import login_required
import pandas as pd
from datetime import datetime
from collections import defaultdict
from django.conf import settings
from dotenv import load_dotenv
import sqlite3
from django.views.generic import View, TemplateView, UpdateView, CreateView
from django.contrib.auth import login, authenticate, get_user_model, logout

from django.shortcuts import render

class LoginView(TemplateView):
        
        template_name = 'app/registration/login.html'
        def post(self, request):
            """Handles POST requests for login, authenticates user."""
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)


class LogoutView(TemplateView):

    template_name = 'registration/logout.html'
    def get(self, request):
        logout(request)
        return render(request, "registration/logout.html", {})
    

@login_required
def prediction_view(request):
    predictions = []
    file_path = settings.BASE_DIR / 'db.sqlite3'
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    if request.method == 'POST':
        if 'checks' in request.POST:
            cursor.execute("UPDATE prediction_app_movies SET 'choice' = 0")

            selected_movies = request.POST.getlist('checks')
            for movie_id in selected_movies:
                cursor.execute("UPDATE prediction_app_movies SET 'choice' = 1 WHERE id = ?", (movie_id,))

            conn.commit()
            return redirect('predict')
        else:
            query = "SELECT DISTINCT title, prediction, image_url, synospis, casting FROM prediction_app_movies"
            df = pd.read_sql_query(query, conn)
            for _, row in df.iterrows():
                prediction = Movies.objects.filter(
                    title=row['title'],
                    prediction=row['prediction'],
                    casting=row['casting'],
                    image_url=row['image_url'],
                    synospis=row['synospis'],
                ).first()  # 1er film trouvé
                if prediction:  
                    predictions.append(prediction)
    
    else:
        query = "SELECT DISTINCT title, prediction, image_url, synospis, casting FROM prediction_app_movies"
        df = pd.read_sql_query(query, conn)
        for _, row in df.iterrows():
            prediction = Movies.objects.filter(
                title=row['title'],
                prediction=row['prediction'],
                casting=row['casting'],
                image_url=row['image_url'],
                synospis=row['synospis'],
            ).first()  # 1er film trouvé
            if prediction:  
                predictions.append(prediction)
    
    conn.close()

    return render(request, 'predictions.html', {'predictions': predictions})


@login_required
def history_view(request):
    history = []
    file_path = settings.BASE_DIR / 'db.sqlite3'
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    if request.method == 'GET':
        query = "SELECT * FROM prediction_app_movies WHERE choice = 1;"
        df = pd.read_sql_query(query, conn)

        for _, row in df.iterrows():
            movies = Movies.objects.filter(
                title=row['title'],
                prediction=row['prediction'],
                casting=row['casting'],
                image_url=row['image_url']
            )

            for movie in movies:
                if movie.title not in [m.title for m in history]:
                    history.append(movie)

    conn.close()

    history_sorted = sorted(history, key=lambda x: x.title, reverse=True)
    return render(request, 'history.html', {'history': history_sorted})

def home_view(request):
    return render(request, 'home.html')


# def custom_404(request, exception=None):
#     return render(request, "404.html", status=404)

# from django.shortcuts import render

# def custom_page_not_found(request, exception):
#     return render(request, '404.html', {}, status=404)