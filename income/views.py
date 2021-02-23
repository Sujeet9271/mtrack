from django.shortcuts import render, redirect
from .models import Income
from django.contrib.auth.decorators import login_required
from .forms import IncomeForm
from django.db.models import Sum
from datetime import datetime
import json
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# @login_required(login_url='/auth/login/')
# def incomes(request):
#     if request.method == "POST":
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')
#         search_incomes = Income.objects.filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('-date')

#         context = {
#             'income': search_incomes
#         }
#         return render(request, 'income.html', context)
#     else:
#         income = Income.objects.filter(user_id=request.user.id).order_by('-date')
#         context = {
#             'income': income,
#         }
#         return render(request, 'income.html', context)

@login_required(login_url='/auth/login/')
def incomes(request):  # Expenditure_detail page
    from_date=request.GET.get('from_date')    
    to_date=request.GET.get('to_date')
    no=request.GET.get('no')

    if request.GET.get('no'):        
        def pages(incomes):
            no=request.GET.get('no')
            page = request.GET.get('page', 1)
            paginator = Paginator(incomes, no)
            try:
                income = paginator.page(page)
                # count= paginator.count
            except PageNotAnInteger:
                income = paginator.page(1)
            except EmptyPage:
                income = paginator.page(paginator.num_pages)
            return income    

        if from_date is None or to_date is None:
            incomes = Income.objects.select_related('user').filter(user_id=request.user.id).order_by('-date')
            income=pages(incomes)
                

            context = {
                'incomes': income                     
                }           
        else:
            if from_date=='' and to_date=='':
                incomes = Income.objects.select_related('user').filter(user_id=request.user.id).order_by('-date')
                income=pages(incomes)
                context = {
                'incomes': income                    
                }
            elif from_date=='' or to_date=='':
                if to_date=='':
                    incomes = Income.objects.select_related('user').filter(user_id=request.user.id, date__gte=from_date).order_by('-date')
                    income=pages(incomes)
                    context = {
                        'incomes': incomes,
                        'from_date':from_date                   
                    }
                elif from_date=='':                
                    incomes = Income.objects.select_related('user').filter(user_id=request.user.id,date__lte=to_date)
                    income=pages(incomes)  
                    context = {
                        'incomes': incomes,
                        
                        'from_date':from_date,
                        'to_date':to_date                    
                    }
                        
            else:
                incomes =  Income.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('-date')
                income=pages(incomes)
                context={
                    'incomes':income,
                    'from_date':from_date,
                    'to_date':to_date
                }
    else:
        if from_date is None or to_date is None:
            incomes = Income.objects.select_related('user').filter(user_id=request.user.id).order_by('-date')
            
            context = {
                'incomes': incomes                     
                }           
        else:
            if from_date=='' and to_date=='':
                incomes = Income.objects.select_related('user').filter(user_id=request.user.id).order_by('-date')
                
                context = {
                'incomes': incomes                    
                }
            elif from_date=='' or to_date=='':
                if to_date=='':
                    incomes = Income.objects.select_related('user').filter(user_id=request.user.id, date__gte=from_date).order_by('-date')
                    
                    context = {
                        'incomes': incomes,
                        'from_date':from_date                   
                    }
                elif from_date=='':                
                    incomes = Income.objects.select_related('user').filter(user_id=request.user.id,date__lte=to_date)                     
                    context = {
                        'incomes': incomes,
                        'from_date':from_date,
                        'to_date':to_date                    
                    }
                        
            else:
                incomes =  Income.objects.select_related('user').filter(user_id=request.user.id, date__range=[from_date, to_date]).order_by('-date')               
                context={
                    'incomes':incomes,
                    'from_date':from_date,
                    'to_date':to_date
                }
    context['no']=no    
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


