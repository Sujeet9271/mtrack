from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='auth_user'),
    path('register/', views.register, name='register'),
    path('dashboard', views.dashboard, name='dashboard'),
<<<<<<< HEAD
    path('logout/', views._logout, name='logout'),
    path('profile/',views.profile, name='profile')
=======
    path('logout/', views._logout, name='logout')
    path('profile/', views.profile, name='profile'),
>>>>>>> 1284e8b53e5b6cf84071e5529ae0132a67a0d0e5
]