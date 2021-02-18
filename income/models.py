from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date


# Create your models here.


class Income(models.Model):
    source = models.CharField(max_length=30)
    income = models.IntegerField(default=0, verbose_name='Income')
    date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source
