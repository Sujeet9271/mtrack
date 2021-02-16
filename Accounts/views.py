from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Sum
from expenses.models import Expenses
from income.models import Income
from.forms import ProfileForm,UserForm




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
                user.profile.save()
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

        from_month = request.POST.get('from_month')
        year = int(from_month[:4])
        print('year',year)
        month=int(from_month[5:])
        # from_date = request.POST.get('from_date')
        # to_date = request.POST.get('to_date')



        income_total = Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('income'))
        expenses_total = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('costs'))

        if income_total['income__sum'] is None:
            income_total['income__sum'] = 0

        if expenses_total['costs__sum'] is None:
            expenses_total['costs__sum'] = 0

        if (income_total['income__sum'] < expenses_total['costs__sum']):
            savings = 0
        else:
            savings = income_total['income__sum'] - expenses_total['costs__sum']

        detail_dict={}
        detail_dict['Expense']= expenses_total['costs__sum']
        detail_dict['Income']= income_total['income__sum']
        detail_dict['Savings']= savings
        details_label=[key for key in detail_dict.keys()]
        details_data=[value for value in detail_dict.values()]

        context = {
            'expenses': expenses_total['costs__sum'],
            'income': income_total['income__sum'],
            'savings': savings,
            'details_label': json.dumps(details_label),
            'details_data': json.dumps(details_data)
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
        
        
        detail_dict={}
        detail_dict['Expense']= expenses['costs__sum']
        detail_dict['Income']= income['income__sum']
        detail_dict['Savings']= savings
        details_label=[key for key in detail_dict.keys()]
        details_data=[value for value in detail_dict.values()]

        context = {
            'expenses': expenses['costs__sum'],
            'income': income['income__sum'],
            'savings': savings,
            'details_label': json.dumps(details_label),
            'details_data': json.dumps(details_data)
        }
        return render(request, 'account/dashboard.html', context)

@login_required(login_url='/auth/login/')
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'account/profile.html', {'user_form': user_form,'profile_form': profile_form})



