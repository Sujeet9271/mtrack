from django.urls import path
from . import views


urlpatterns=[
    path('',views.dashboard,name="dashboard"),
    path('old/',views.dashboard1,name="dashboardold"),
    path('api/', views.dashboardapi, name='dashboardapi')
]