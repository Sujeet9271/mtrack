from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='auth_user'),
    path('register/', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout/', views._logout, name='logout'),]
