from django.urls import path
from . import views


urlpatterns = [
    path('', views.expenses, name='expenses'),
    path('expenses_home/', views.expenses_home, name='expenses_home'),
    path('category/', views.exp_category, name='exp_category'),
    path('create/', views.create, name='exp_create'),
    path('edit/<int:id>', views.edit, name='exp_edit'),
    path('_delete/<int:id>', views.exp_delete, name='exp_delete'),
    path('category/delete/<int:id>', views.delete_category, name='category_delete')
]