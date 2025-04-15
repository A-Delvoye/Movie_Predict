from django.urls import path
from users.views import signup, home_view
from django.urls import path, include
from django.contrib.auth import views as auth_views
from prediction_app import views as custom_views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

]