from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.log_in, name='auth_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.profile_delete,name="profile_delete"),
]
