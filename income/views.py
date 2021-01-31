from django.shortcuts import render, redirect
from .models import Income
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from django.db.models import Sum
import datetime


@login_required(login_url='/auth/login/')
def incomes(request):
    if request.method == "POST":

        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        search_incomes = Income.objects.filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('date')


        # month=str(request.POST.get('month'))    #to extract month, month[5:]
        # search_incomes_bymonth = Income.objects.filter(user_id=request.user.id, date__month=month[5:]).order_by('date')

        context = {
            'income': search_incomes,

            # 'income_month': search_incomes_bymonth,
        }
        return render(request, 'income.html', context)
    else:
        income = Income.objects.filter(user_id=request.user.id).order_by('date') # Select * from income_income

        context = {
            'income': income,
        }
        return render(request, 'income.html', context)


@login_required(login_url='/auth/login/')
def incomes_home(request):
    x = datetime.datetime.now()
    x = x.strftime("%W")  # to get current week
    print(x)

    income = Income.objects.select_related().filter(user_id=request.user.id, date__week=x)
    print(income)
    return render(request, 'incomes/income_home.html',{'income':income})


@login_required(login_url='/auth/login/')
def create(request):
    if request.method == 'GET':
        context = {
            'form': IncomeForm(request.user.id)
        }
        return render(request, 'incomes/create.html', context)
    else:
        form = IncomeForm(request.user.id, request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            context = {
                'msg': 'Added Successfully',
                'form': form,
            }

            return render(request, 'incomes/create.html', context)
        else:
            context = {
                'errmsg': 'Could not Add',
                'form': form,
            }
            return render(request, 'incomes/create.html', context)


@login_required(login_url='/auth/login/')
def edit(request, id):
    data = Income.objects.get(pk=id)
    form = IncomeForm(request.user.id, request.POST or None, instance=data)
    if form.is_valid():
        form.save()
        context = {
            'form': form,
            'msg': 'Edited Successfully!!'
        }
        return render(request, 'incomes/edit.html', context)
    return render(request, 'incomes/edit.html', {'form': form})

@login_required(login_url='/auth/login/')
def inc_delete(request, id):
    try:
        a = Income.objects.get(pk=id)
        a.delete()
        return redirect('incomes')

    except:
        return redirect('incomes')


@login_required(login_url='/auth/login/')
def total_income(request, id):
    total = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
    context = {'total': total}
    return render(request, 'income.html', context)
