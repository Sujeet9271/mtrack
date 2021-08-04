from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    
    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path('auth/', include('Accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
]
