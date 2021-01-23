from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from expenses.models import Expenses
from income.models import Income




def login(request):
    if request.method == 'GET':
        return render(request, 'account/login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            context = {
                'errmsg': 'Username or Password is Wrong'
            }
            return render(request, 'account/login.html', context)



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'User with same email exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, first_name=first_name, last_name=last_name, email=email)
                user.save()
                messages.info(request, "Registered successfully")
                return redirect('auth_user')
        else:
            messages.error(request, "Confirmed Password doesn't match")
            return redirect('register')
    else:
        return render(request, 'account/register.html')


def _logout(request):
    logout(request)
    return redirect('auth_user')


@login_required(login_url='/auth/login/')
def dashboard(request):
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')


        income = Income.objects.filter(user_id=request.user.id, date__range=[from_date, to_date]).aggregate(Sum('income'))
        expenses = Expenses.objects.filter(user_id=request.user.id, date__range=[from_date, to_date]).aggregate(Sum('costs'))

        if income['income__sum'] is None:
            income['income__sum'] = 0
        if expenses['costs__sum'] is None:
            expenses['costs__sum'] = 0

        if (income['income__sum'] < expenses['costs__sum']):
            savings = 0
        else:
            savings = income['income__sum'] - expenses['costs__sum']

        context = {
            'expenses': expenses['costs__sum'],
            'income': income['income__sum'],
            'savings': savings,
        }
        return render(request, 'account/dashboard.html', context)

    else:
        income = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
        expenses = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))

        if income['income__sum'] is None:
            income['income__sum'] = 0
        if expenses['costs__sum'] is None:
            expenses['costs__sum'] = 0

        if (income['income__sum'] < expenses['costs__sum']):
            savings = 0
        else:
            savings = income['income__sum'] - expenses['costs__sum']
        context = {
            'expenses': expenses['costs__sum'],
            'income': income['income__sum'],
            'savings': savings,
        }
        return render(request, 'account/dashboard.html',context)

