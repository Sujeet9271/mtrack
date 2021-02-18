from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from .models import Expenses, Category
from django.contrib.auth.decorators import login_required
from .forms import ExpensesForm
from datetime import datetime
import json




@login_required(login_url='/auth/login/')
def expenses(request):  # Expenditure_detail page
    from_date=request.GET.get('from_date')
    
    to_date=request.GET.get('to_date')
    

    if from_date is None or to_date is None:
        expenses = Expenses.objects.select_related('user').filter(user_id=request.user.id).order_by('timestamp')
        total = Expenses.objects.select_related('user').filter(user_id=request.user.id).aggregate(Sum('costs'))
        context = {
        'expenses': expenses,'total':total['costs__sum']                     
        }           
    else:
        if from_date=='' and to_date=='':
            expenses = Expenses.objects.select_related('user').filter(user_id=request.user.id).order_by('timestamp')
            total = Expenses.objects.select_related('user').filter(user_id=request.user.id).aggregate(Sum('costs'))
            context = {
            'expenses': expenses,'total':total['costs__sum']                     
            }
        elif from_date=='' or to_date=='':
            if to_date=='':
                expenses = Expenses.objects.select_related('user').filter(user_id=request.user.id, date__gte=from_date).order_by('date')
                total=Expenses.objects.select_related('user').filter(user_id=request.user.id, date__gte=from_date).aggregate(Sum('costs'))
                context = {
                    'expenses': expenses,
                    'from_date':from_date,'total':total['costs__sum']                    
                }
            elif from_date=='':                
                expenses = Expenses.objects.select_related('user').filter(user_id=request.user.id,date__lte=to_date)
                total=Expenses.objects.select_related('user').filter(user_id=request.user.id, date__lte=to_date).aggregate(Sum('costs'))
                context = {
                    'expenses': expenses,
                    ' total':total['costs__sum'] ,
                    'from_date':from_date,
                    'to_date':to_date                    
                }
                    
        else:
            expenses =  Expenses.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('date')
            total = Expenses.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).aggregate(Sum('costs'))
            context={
                'expenses':expenses,
                'total':total['costs__sum'],
                'from_date':from_date,
                'to_date':to_date
            }
    
    return render(request, 'expenses.html', context)


@login_required(login_url='/auth/login/')
def expenses_home(request):
    today=datetime.now()
    current_month=today.month
    current_year=today.year
    expenses = Expenses.objects.filter(user_id=request.user.id, date__year=current_year,date__month=current_month).order_by('timestamp')
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
        user=request.user.id
        expense=request.POST
        form = ExpensesForm(user,expense)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            messages.success(request,'Added Successfully!!')
            return redirect('expenses_home')
        else:
            context = {
                'errmsg': 'Could not Add',
                'form': form,
            }
            return render(request, 'expenses/create.html', context)


@login_required(login_url='/auth/login/')
def edit(request, id):
    data = Expenses.objects.get(pk=id)
    form = ExpensesForm(request.user.id, instance=data)
    if request.method=="POST":
        form = ExpensesForm(request.user.id, request.POST or None, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request,'Edited Sucessfully!!')            
            return redirect('expenses_home')
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



