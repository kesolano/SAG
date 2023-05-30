from django.conf import settings
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('home/', views.home, name="home"),

    path('register/', views.register, name="register"),

    path('home/prediccion_probabilidad/',
         views.prediccion_probabilidad, name="prediccion_probabilidad"),

    path('login/', LoginView.as_view(template_name = "app/login.html"), name="login"),

    path('logout/', LogoutView.as_view(template_name="app/logout.html"), name="logout"),

] 