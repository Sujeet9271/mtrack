from django.contrib import admin
from .models import Income

# Register your models here.

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display=['id','income','source','user_id','user']
