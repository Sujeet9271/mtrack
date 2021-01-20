from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from expenses.models import Expenses
from income.models import Income

@login_required(login_url='/auth/login/')
def home(request):
    income = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
    expenses = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))
    if income['income__sum'] is None:
        income['income__sum']=0
    if expenses['costs__sum'] is None:
        expenses['costs__sum']=0

    if (income['income__sum'] < expenses['costs__sum']):
        savings = 0
    else:
        savings = income['income__sum'] - expenses['costs__sum']
    context = {
        'expenses': expenses['costs__sum'],
        'income': income['income__sum'],
        'savings': savings,
    }
    return render(request, 'index.html',context)

def developing(request):
    return render(request,'developing.html')

def money_details(request):
    income = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
    expenses = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))
    savings = income['income__sum']-expenses['costs__sum']
    context = {
        'Money Detail': 'Money Detail',
        'expenses': expenses['costs__sum'],
        'income': income['income__sum'],
        'savings': savings,
    }
    return render(request, 'money.html', context)

