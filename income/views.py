from django.shortcuts import render, redirect
from .models import Income
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from django.db.models import Sum
from datetime import date,datetime
import json
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def incomeChart(incomes):
    incomedata = {}
    def source_sum(source): 
        inc = incomes.filter(source=source).aggregate(Sum('income'))       
        return inc['income__sum']
    
    source_list=[]
    for income in incomes:
        source_list.append(income.source)       

    source_list=list(set(source_list))
        
    for income in incomes:
        for source in source_list:
            incomedata[source]=source_sum(source)

    sources=[source for source in incomedata.keys()]
    amount=[amount for amount in incomedata.values()] 
    return {'sources':sources,'amount':amount}

def pages(incomes,no,page):
    data = incomeChart(incomes=incomes)
    sources = data['sources']
    amount = data['amount']
    paginator = Paginator(incomes, no)
    try:
        income = paginator.page(page)
    except PageNotAnInteger:
        income = paginator.page(1)
    except EmptyPage:
        income = paginator.page(paginator.num_pages)
    return income,sources,amount


@login_required(login_url='/auth/login/')
def incomes(request):  # Expenditure_detail page
    from_date=request.GET.get('from_date',f'{date.today().year}-01-01')    
    to_date=request.GET.get('to_date',str(date.today()))

    context={}
    if from_date=='' or to_date=='':
        from_date=f'{date.today().year}-01-01'    
        to_date=str(date.today())

    no = request.GET.get('no')   
    page = request.GET.get('page', 1)

    if request.GET.get('no'):        
        query =  Income.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('date')
        queryset=pages(incomes=query,page=page,no=no)
        incomes = queryset[0]
        sources = queryset[1]
        amount = queryset[2]
    else:
        incomes =  Income.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('date')               
        data = incomeChart(incomes)
        sources = data['sources']
        amount = data['amount']

    context['no']=no    
    context['from_date'] = from_date
    context['to_date'] = to_date
    context['incomes'] =incomes 
    context['source'] = sources
    context['amount'] =amount
    return render(request, 'income.html', context)


@login_required(login_url='/auth/login/')
def incomes_home(request):
    today=datetime.now()
    current_year=today.year
    current_month=today.month
    incomes = Income.objects.filter(user_id=request.user.id, date__year=current_year,date__month=current_month).order_by('-date')   

    data=incomeChart(incomes)

    context={
        'income':incomes,
        'month': today.strftime('%B'),
        'sources':data['sources'],
        'amount':data['amount']
    }

    return render(request, 'incomes/income_home.html',context)




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
            messages.success(request,'Income Added Successfully')
            return redirect('income_home')
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
    context={}
    context['form'] = form
    if request.method=='POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Edited Successfully')
            return redirect('incomes_home')
        messages.error(request,'Failed to update')
    return render(request, 'incomes/edit.html', context)

@login_required(login_url='/auth/login/')
def inc_delete(request, id):
    try:
        a = Income.objects.get(pk=id)
        a.delete()
        return redirect('incomes')

    except:
        return redirect('incomes')


