from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import ProfileForm,UserForm
from expenses.models import Expenses,Category
from income.models import Income





def login(request):
    if request.method == 'GET':
        return render(request, 'account/login.html')
    else:
        u = request.POST.get('username')
        p = request.POST.get('password')
        check=User.objects.filter(username=u).exists()
        if check==False:
            context = {
                'errmsg': 'User doesnot exists'
                }
            return render(request, 'account/login.html', context)
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
            return render(request,'account/login',{'msg': 'Registered Successfully'})
        else:
            messages.error(request, "Confirmed Password doesn't match")
            return redirect('register')
    else:
        return render(request, 'account/register.html')


def _logout(request):
    logout(request)
    return redirect('auth_user')


@login_required(login_url='auth_user')
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
        income=Income.objects.filter(user_id=request.user.id).count()
        expense=Expenses.objects.filter(user_id=request.user.id).count()
        category=Category.objects.filter(user_id=request.user.id).count()

    return render(request, 'account/profile.html', {'user_form': user_form,'profile_form': profile_form,'income':income,'expense':expense,'category':category})

@login_required(login_url='auth_user')
def profile_delete(request):
    income=Income.objects.filter(user_id=request.user.id).count()
    expense=Expenses.objects.filter(user_id=request.user.id).count()
    u = User.objects.get(id=request.user.id)
    u.delete()
    messages.success(request, "Account deleted successfully")
    return redirect('auth_user')
        

