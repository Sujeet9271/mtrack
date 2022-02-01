from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib import messages
from .models import Expenses, Category
from django.contrib.auth.decorators import login_required
from .forms import ExpensesForm
from datetime import datetime
import json
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from datetime import date

def expenseChart(expenses,categories):
    data = {}
    def category_sum(category):
        cost = expenses.filter(category__title=category).aggregate(Sum('costs'))          
        return cost['costs__sum']

    for expense in expenses:
        for category in categories:
            data[category]=category_sum(category)


    categories=[category for category in data.keys()]
    amount=[amount for amount in data.values()]  
    return {'category':categories,'amount':amount} 

def pages(expenses,page,no,categories):
    amount=[]
    for category in categories:
        expense = expenses.filter(category__title=category).aggregate(Sum('costs'))
        amount.append(expense['costs__sum'] if expense['costs__sum'] is not None else 0)

    paginator = Paginator(expenses, no)
    try:
        expense = paginator.page(page)
    except PageNotAnInteger:
        expense = paginator.page(1)
    except EmptyPage:
        expense = paginator.page(paginator.num_pages)

    return expense,amount 


@login_required(login_url='/auth/login/')
def expenses(request):  # Expenditure_detail page

    from_date=request.GET.get('from_date',f'{date.today().year}-01-01')    
    to_date=request.GET.get('to_date',str(date.today()))

    context={}
    if from_date=='' or to_date=='':
        from_date=f'{date.today().year}-01-01'    
        to_date=str(date.today())

    no = request.GET.get('no')   
    page = request.GET.get('page', 1)
    categories = list(Category.objects.filter(user_id=request.user.id).values_list('title',flat=True))

    if no:    
        query =  Expenses.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('-date')
        queryset=pages(query,page,no,categories)
        expenses=queryset[0]
        amount=queryset[1]
    else:
        expenses =  Expenses.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('-date')
        amount=[]
        for category in categories:
            expense = expenses.filter(category__title=category).aggregate(Sum('costs'))
            amount.append(expense['costs__sum'] if expense['costs__sum'] is not None else 0)

    context['categories'] = categories
    context['no']=no
    context['from_date'] = from_date
    context['to_date'] = to_date
    context['expenses'] =expenses 
    context['amount'] =amount

    return render(request, 'expenses.html', context)



@login_required(login_url='/auth/login/')
def expenses_home(request):
    today=datetime.now()
    current_month=today.month
    current_year=today.year
    expenses = Expenses.objects.filter(user_id=request.user.id, date__year=current_year,date__month=current_month).order_by('-date') 
    categories= Category.objects.filter(user_id=request.user.id).values_list('title',flat=True)
    data=expenseChart(expenses,categories)  

    context={
        'expense': expenses,
        'month':today.strftime('%B'),
        'categories':json.dumps(data['category']),
        'amount': json.dumps(data['amount'])
        } 

    return render(request, 'expenses/expenses_home.html', context)



@login_required(login_url='/auth/login/')
def exp_category(request):  # Category Page
    category = Category.objects.filter(user_id=request.user.id)
    if request.method == 'GET':
        context = {
            'data': category
        }
        return render(request, 'expenses/exp_category.html', context)
    else:
        t = request.POST.get('title')
        c = Category(title=t, user=request.user)
        try:
            c.save()
            context = {
                'msg': 'Added Successfully',
                'data': category
            }
            return render(request, 'expenses/exp_category.html', context)
        except:
            context = {
                'data': category,
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
    context={}
    data = Expenses.objects.get(pk=id)
    form = ExpensesForm(request.user.id, request.POST or None, instance=data)
    context['form'] = form
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Edited Sucessfully!!')            
            return redirect('expenses_home')
        messages.error(request,'Failed to update')
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



