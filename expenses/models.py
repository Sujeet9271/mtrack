from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class Expenses(models.Model):
    title = models.CharField(max_length=30,)
    costs = models.IntegerField(verbose_name='total cost',default=0)
    description = models.TextField(null=True, blank=True, )
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False, blank=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

