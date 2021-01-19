from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login/')
def home(request):
    return render(request, 'index.html')

def developing(request):
    return render(request,'developing.html')