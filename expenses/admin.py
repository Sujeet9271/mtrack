from django.contrib import admin
from .models import Category,Expenses
# Register your models here.
# admin.site.register(Category)
# admin.site.register(Expenses)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','title','user_id','user']

@admin.register(Expenses)
class ExpenseAdmin(admin.ModelAdmin):
    list_display=['id','title','costs','description','category','user_id','user' ]
