from django.urls import path
from .views import prediction_view, history_view

urlpatterns = [
    path('predict/', prediction_view, name='predict'),
    path('history/', history_view, name='history')]
