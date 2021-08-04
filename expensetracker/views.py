from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required



# @login_required(login_url='/auth/login/')
def home(request):   
    if request.user.is_authenticated:
        return redirect('dashboard') 
    else:
        return render(request, 'index.html')


