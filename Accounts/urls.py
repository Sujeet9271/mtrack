from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='auth_user'),
    path('register/', views.register, name='register'),
    path('logout/', views._logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
