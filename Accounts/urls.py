from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import urls

urlpatterns = [
    path('login/', views.log_in, name='auth_user'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='log_out'),
    path('profile/', views.profile, name='profile'),
    path('delete/', views.profile_delete,name="profile_delete"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'), 
]
