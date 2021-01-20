from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth


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


# def login(request):
#     if request.method=="POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, 'Username or Password incorrect')
#             return redirect('login')
#     else:
#         return render(request, 'account/login.html')


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
                user.save();
                messages.info(request, "Registered successfully")

            return redirect('auth_user')
        else:
            messages.error(request, "Confirmed Password doesn't match")
            return redirect('register')


    else:
        return render(request, 'account/register.html')

@login_required(login_url='/auth/login/')
def dashboard(request):
    return render(request, 'account/dashboard.html')

def _logout(request):
    logout(request)
    return redirect('auth_user')






