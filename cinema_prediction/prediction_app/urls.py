from django.urls import path
from .views import prediction_view, history_view, LogoutView, LoginView
# from .views import custom_404 
from django.conf import settings
from django.conf.urls import handler404

urlpatterns = [
    path('predict/', prediction_view, name='predict'),
    path('history/', history_view, name='history'),
    path('registration/login/', LoginView.as_view(), name='login'),
    path('registration/login/', LogoutView.as_view(), name='logout')    

    ]

if settings.DEBUG:
    handler404 = 'views.custom_404'