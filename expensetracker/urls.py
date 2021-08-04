from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name="dashboard"),
    path('expenses/', include('expenses.urls')),
    path('income/', include('income.urls')),
    path('auth/', include('Accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
]
