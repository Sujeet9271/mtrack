from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from expenses.views import expenseChart
from expenses.models import Expenses,Category
from income.models import Income
from income.views import incomeChart
from .forms import DateForm
import json,datetime
from django.http import JsonResponse
from django.db import connection
from django.db.models.functions import TruncMonth



#using get and post method in django framework

def dashboard(request):
    if request.method == "POST":
        from_month = request.POST.get('from_month')
        year = int(from_month[:4])
        month= int(from_month[5:])

        month_name=datetime.date(year,month,1).strftime('%B %Y')

        month_list=[datetime.date(year,month,1).strftime('%B')]

        incomes_list=[Income.objects.select_related('user').filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('income'))['income__sum']]
        expenses_list=[Expenses.objects.select_related('user').filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('costs'))['costs__sum']]
        
        if incomes_list[0] is None:
            incomes_list[0] = 0

        if expenses_list[0] is None:
            expenses_list[0] = 0


        savings_list = [incomes_list[0]-expenses_list[0] if incomes_list[0]>expenses_list[0] else 0]

        expenses = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month)
        categories = Category.objects.filter(user_id=request.user.id)

        incomes=Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month)

        incomedata=incomeChartapi(incomes)
        expensedata=expenseChartapi(expenses,categories)
        
        context = {
            'month_list':json.dumps(month_list),
            'month':month_name,
            'expenses_list':json.dumps(expenses_list),
            'incomes_list':json.dumps(incomes_list),
            'savings_list':json.dumps(savings_list),
            'total_income':json.dumps(incomes_list[0]),
            'total_expenses':json.dumps(expenses_list[0]),
            'total_savings':json.dumps(savings_list[0]),
            "expenses":json.dumps(expensedata),
            "incomes":json.dumps(incomedata),                       
        }

        return render(request, 'account/dashboard.html', context)

    else:
        

        income_by_month=[data for data in Income.objects.filter(user_id=request.user.id).values('date__month').annotate(Income=Sum('income'))]       
        expense_by_month=[data for data in Expenses.objects.filter(user_id=request.user.id).values('date__month').annotate(Expense=Sum('costs'))]

        income_month={}
        for data in Income.objects.filter(user_id=request.user.id).values('date__month').annotate(Income=Sum('income')):
            month=data['date__month']           
            income_month[month]=data['Income']        
        

        expense_month={}
        for data in Expenses.objects.filter(user_id=request.user.id).values('date__month').annotate(Expense=Sum('costs')):
            month=data['date__month']  
            expense_month[month]=data['Expense']

        total_income_month=[month for month in income_month.keys()]
        total_expense_month=[month for month in expense_month.keys()]

        total_month= list(set(total_expense_month+total_income_month))
        
        detail_by_month={}
        for m in total_month:
            month=datetime.date(2000,m,1).strftime('%B')
            detail_by_month[month]={} 
            if m in income_month.keys() and expense_month.keys():
                    detail_by_month[month]['Expenses']=expense_month[m] if m in expense_month.keys() else 0
                    detail_by_month[month]['Incomes']=income_month[m] if m in income_month.keys() else 0                 
                    detail_by_month[month]['Savings']=(detail_by_month[month]['Incomes']- detail_by_month[month]['Expenses']) if detail_by_month[month]['Incomes']>detail_by_month[month]['Expenses'] else 0
            elif m not in income_month.keys():
                detail_by_month[month]['Incomes']= 0
                detail_by_month[month]['Expenses']=expense_month[m]
                detail_by_month[month]['Savings']=0
            elif m not in expense_month.keys():
                detail_by_month[month]['Expenses']= 0
                detail_by_month[month]['Incomes']=income_month[m]
                detail_by_month[month]['Savings']=income_month[m]
          
        expenses = Expenses.objects.filter(user_id=request.user.id)
        categories = Category.objects.filter(user_id=request.user.id)

        incomes=Income.objects.filter(user_id=request.user.id)

        incomedata=incomeChartapi(incomes)
        expensedata=expenseChartapi(expenses,categories)

        expenses_list=[]
        incomes_list=[]
        savings_list=[]
        month_list=[]
        for key in detail_by_month.keys():
            month_list.append(key)
            expenses_list.append(detail_by_month[key]['Expenses'])
            incomes_list.append(detail_by_month[key]['Incomes'])
            savings_list.append(detail_by_month[key]['Savings'])
            
        total_income=sum(incomes_list)
        total_expense=sum(expenses_list)
        total_savings=sum(savings_list)
        
       
        income_year=[]
        for data in Income.objects.filter(user_id=request.user.id).values('date__year'):
            income_year.append(data['date__year'])                     
                    
        expense_year=[]
        for data in Expenses.objects.filter(user_id=request.user.id).values('date__year'):
            expense_year.append(data['date__year'])  
        
        total_year=list(set(income_year+expense_year)) 

        context = {
            'monthlydetail':json.dumps('true'),
            'month_list':json.dumps(month_list),
            'year':total_year,
            'expenses_list':json.dumps(expenses_list),
            'incomes_list':json.dumps(incomes_list),
            'savings_list':json.dumps(savings_list),
            'total_income':json.dumps(total_income),
            'total_expenses':json.dumps(total_expense),
            'total_savings':json.dumps(total_savings),
            "expenses":json.dumps(expensedata),
            "incomes":json.dumps(incomedata),    
                              
        }
        print(context)

        return render(request, 'account/dashboard.html', context)


#using dashboardapi view for data
@login_required(login_url='/auth/login/')
def dashboardapiview(request):
    return render(request,'account/dashboard_.html')

@login_required(login_url='/auth/login/')
# def dashboardapi(request):    
#     if request.GET.get('from_month'):
#         from_month=request.GET.get('from_month')
#         year = int(from_month[:4])
#         month=int(from_month[5:])

#         month_name=datetime.date(year,month,1).strftime('%B %Y')

#         income = Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('income'))
#         expense = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('costs'))        

#         expenses = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month)
#         categories = Category.objects.filter(user_id=request.user.id)

#         incomes=Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month)
#     else:
#         month_name=''
#         income = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
#         expense = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))

#         income_total = Income.objects.filter(user_id=request.user.id).values('date__month').annotate(total=Sum('income'))
#         income_by_month=[data for data in income_total]
#         income_month={}
#         for data in income_by_month:
#             month=datetime.date(2000,data['date__month'],1).strftime('%B')
#             income_month[month]=data['total']
#         print(income_month)

#         expense_total = Expenses.objects.filter(user_id=request.user.id).values('date__month').annotate(total=Sum('costs'))
#         expense_by_month=[data for data in expense_total]
#         expense_month={}
#         for data in expense_by_month:
#             month=datetime.date(2000,data['date__month'],1).strftime('%B')
#             expense_month[month]=data['total']
#         print(income_month)           
            

#         expenses = Expenses.objects.filter(user_id=request.user.id)
#         categories = Category.objects.filter(user_id=request.user.id)

#         incomes=Income.objects.filter(user_id=request.user.id)

#     incomedata=incomeChartapi(incomes)
#     expensedata=expenseChartapi(expenses,categories)

#     if income['income__sum'] is None:
#         income['income__sum'] = 0

#     if expense['costs__sum'] is None:
#         expense['costs__sum'] = 0

#     if (income['income__sum'] < expense['costs__sum']):
#         savings = 0
#     else:
#         savings = income['income__sum'] - expense['costs__sum']       
    
#     detail_dict={}
#     detail_dict['Expense']= expense['costs__sum']
#     detail_dict['Income']= income['income__sum']
#     detail_dict['Savings']= savings
    
#     context = {
#         "details":detail_dict,
#         "expenses":expensedata,
#         "incomes":incomedata,
#         "month":month_name ,
#         "income_by_month":income_month,
#         "expense_by_month":expense_month      
#     }
    
#     return JsonResponse(context)

def dashboardapi(request):    
    if request.GET.get('from_month'):
        from_month=request.GET.get('from_month')
        year = int(from_month[:4])
        month=int(from_month[5:])

        month_name=datetime.date(year,month,1).strftime('%B %Y')

        income = Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('income'))
        expense = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month).aggregate(Sum('costs'))        

        expenses = Expenses.objects.filter(user_id=request.user.id,date__year=year, date__month=month)
        categories = Category.objects.filter(user_id=request.user.id)

        incomes=Income.objects.filter(user_id=request.user.id,date__year=year, date__month=month)
        incomedata=incomeChartapi(incomes)
        expensedata=expenseChartapi(expenses,categories)
        if income['income__sum'] is None:
            income['income__sum'] = 0

        if expense['costs__sum'] is None:
            expense['costs__sum'] = 0

        if (income['income__sum'] < expense['costs__sum']):
            savings = 0
        else:
            savings = income['income__sum'] - expense['costs__sum']
            
        
        detail_dict={}
        detail_dict['Expense']= expense['costs__sum']
        detail_dict['Income']= income['income__sum']
        detail_dict['Savings']= savings        
        
        context = {
            "details":detail_dict,
            "expenses":expensedata,
            "incomes":incomedata,
            "month":month_name ,
                   }
        
        return JsonResponse(context)
    else:
        month_name=''
        income = Income.objects.filter(user_id=request.user.id).aggregate(Sum('income'))
        expense = Expenses.objects.filter(user_id=request.user.id).aggregate(Sum('costs'))

        
        income_by_month=[data for data in Income.objects.filter(user_id=request.user.id).values('date__month').annotate(Income=Sum('income'))]
       
        expense_by_month=[data for data in Expenses.objects.filter(user_id=request.user.id).values('date__month').annotate(Expense=Sum('costs'))]


        income_month={}
        for data in Income.objects.filter(user_id=request.user.id).values('date__month').annotate(Income=Sum('income')):
            month=data['date__month']           
            income_month[month]=data['Income']        
        

        expense_month={}
        for data in Expenses.objects.filter(user_id=request.user.id).values('date__month').annotate(Expense=Sum('costs')):
            month=data['date__month']  
            expense_month[month]=data['Expense']

        total_income_month=[month for month in income_month.keys()]
        total_expense_month=[month for month in expense_month.keys()]

        total_month=total_expense_month+total_income_month

        
        detail_by_month={}
        for m in total_month:
            month=datetime.date(2000,m,1).strftime('%B')
            detail_by_month[month]={} 
            if m in income_month.keys() and expense_month.keys():
                    detail_by_month[month]['Expenses']=expense_month[m]
                    detail_by_month[month]['Incomes']=income_month[m]                    
                    detail_by_month[month]['Savings']=(income_month[m]- expense_month[m]) if income_month[m]>expense_month[m] else 0
            else:
                if m in income_month.keys():
                    detail_by_month[month]['Expenses']=0
                    detail_by_month[month]['Incomes']=income_month[m]                    
                    detail_by_month[month]['Savings']=(income_month[m]- expense_month[m]) if income_month[m]>expense_month[m] else 0
                elif m in expense_month.keys():
                    detail_by_month[month]['Expenses']=expense_month[m]
                    detail_by_month[month]['Incomes']=0
                    detail_by_month[month]['Savings']=0
                

            

        expenses = Expenses.objects.filter(user_id=request.user.id)
        categories = Category.objects.filter(user_id=request.user.id)

        incomes=Income.objects.filter(user_id=request.user.id)

        incomedata=incomeChartapi(incomes)
        expensedata=expenseChartapi(expenses,categories)

            
        
        # detail_dict={}
        # detail_dict['Expense']= expense['costs__sum']
        # detail_dict['Income']= income['income__sum']
        # detail_dict['Savings']= savings

        
        
        context = {
            # "details":detail_dict,
            "detail_by_month":detail_by_month,
            "expenses":expensedata,
            "incomes":incomedata,
            "month":month_name ,
            "income_by_month":income_month,
            "expense_by_month":expense_month
        }
        
        return JsonResponse(context)


def expenseChartapi(expenses,categories):
    data = {}
    def category_sum(category):
        cost = expenses.filter(category__title=category).aggregate(Sum('costs'))          
        return cost['costs__sum']

    categories=[category.title for category in categories]

    for expense in expenses:
        for category in categories:
            data[category]=category_sum(category)
    
    return data


def incomeChartapi(incomes):
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

    
    return incomedata