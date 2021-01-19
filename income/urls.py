from django.urls import path
from . import views

urlpatterns = [
    path('', views.incomes, name='incomes'),
    path('income_home/', views.incomes_home, name='income_home'),
    path('inc/', views.incomes, name='income_details'),
    path('create/', views.create, name='inc_create'),
    path('edit/<int:id>', views.edit, name='inc_edit'),
    path('_delete/<int:id>', views.inc_delete, name='inc_delete'),

]