from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from expenses.models import Expenses
from income.models import Income

# @login_required(login_url='/auth/login/')
def home(request):    
    return render(request, 'index.html')


