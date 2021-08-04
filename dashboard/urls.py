from django.urls import path
from . import views


urlpatterns=[
    path("",views.views.dashboard,name='dashboard'),
    path('new/',views.dashboardapiview,name="dashboardapiview"),
    path('api/', views.dashboardapi, name='dashboardapi')
]