from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Expenses, Category
from django.contrib.auth.decorators import login_required
from .forms import ExpensesForm
from datetime import datetime
import json




@login_required(login_url='/auth/login/')
def expenses(request):  # Expenditure_detail page
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        # search_expenses=Expenses.objects.raw('select id,title,costs,description,date from expenses_expenses where date between "'+from_date+'" and "'+to_date+'" order by"'+from_date+ '"')
        search_expenses = Expenses.objects.select_related().filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('date')
        total = Expenses.objects.select_related().filter(user_id=request.user.id, date__range=[from_date, to_date]).aggregate(Sum('costs'))


        context = {
            'expenses': search_expenses,
            'total': total['costs__sum'],
        }
        return render(request, 'expenses.html', context)
    else:
        expenses = Expenses.objects.select_related().filter(user_id=request.user.id).order_by('date')
        total = Expenses.objects.select_related().filter(user_id=request.user.id).aggregate(Sum('costs'))
        # Select * from Expenses
        context = {
            'expenses': expenses,
            'total': total['costs__sum'],
        }
        return render(request, 'expenses.html', context)


@login_required(login_url='/auth/login/')
def expenses_home(request):
    today=datetime.now()
    current_month=today.month
    current_year=today.year
    expenses = Expenses.objects.filter(user_id=request.user.id, date__year=current_year,date__month=current_month)
    data = {}

    def category_sum(category):
        cost = expenses.filter(category__title=category).aggregate(Sum('costs'))          
        return cost['costs__sum']

    categories=[category.title for category in Category.objects.filter(user_id=request.user.id)]

    for expense in expenses:
        for category in categories:
            data[category]=category_sum(category)


    categories=[category for category in data.keys()]
    amount=[amount for amount in data.values()] 

    print(categories,amount)    


    return render(request, 'expenses/expenses_home.html', {'expense': expenses,'month':today.strftime('%B'),'categories':json.dumps(categories),'amount': json.dumps(amount)})


@login_required(login_url='/auth_user')
def exp_category(request):  # Category Page
    data = Category.objects.filter(user_id=request.user.id)
    if request.method == 'GET':
        context = {
            'data': data
        }
        return render(request, 'expenses/exp_category.html', context)
    else:
        t = request.POST.get('title')
        c = Category(title=t, user=request.user)
        try:
            c.save()
            context = {
                'msg': 'Added Successfully',
                'data': data
            }
            return render(request, 'expenses/exp_category.html', context)
        except:
            context = {
                'data': data,
                'errmsg': 'Currently Unable to insert data'
            }
            return render(request, 'expenses/exp_category.html', context)




@login_required(login_url='/auth/login/')
def create(request):  # Adding Expense

    if request.method == 'GET':
        context = {
            'form': ExpensesForm(request.user.id)
        }
        return render(request, 'expenses/create.html', context)
    else:
        form = ExpensesForm(request.user.id, request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            context = {
                'msg': 'Added Successfully',
                'form': ExpensesForm(request.user.id),
            }
            return render(request, 'expenses/create.html', context)
        else:
            context = {
                'errmsg': 'Could not Add',
                'form': form,
            }
            return render(request, 'expenses/create.html', context)


@login_required(login_url='/auth/login/')
def edit(request, id):
    data = Expenses.objects.get(pk=id)
    form = ExpensesForm(request.user.id, request.POST or None, instance=data)
    if form.is_valid():
        form.save()
        context = {
            'form': form,
            'msg': 'Edited Successfully!!'
        }
        return render(request, 'expenses/edit.html', context)
    return render(request, 'expenses/edit.html',{'form':form})


@login_required(login_url='/auth/login/')
def exp_delete(request, id):
    try:
        a = Expenses.objects.get(pk=id)
        a.delete()
        return redirect('expenses')
    except:
        return redirect('expenses')


@login_required(login_url='/auth/login/')
def delete_category(request, id):
    a = Category.objects.get(id=id)
    a.delete()
    return redirect('exp_category')


@login_required(login_url='/auth/login/')
def total_expense(request, id):
    total = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))
    context = {'total': total}
    return render(request, 'expenses.html', context)
