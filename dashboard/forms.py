from django.forms import ModelForm
from expenses.models import Expenses
from income.models import Income
from django import forms



class DateForm(forms.Form):
    income_month=[]
    for data in Income.objects.filter().values('date__month'):
        income_month.append(data['date__month'])                     
                
    expense_month=[]
    for data in Expenses.objects.filter().values('date__month'):
        expense_month.append(data['date__month'])  
        
    total_month= list(set(expense_month+income_month))

    income_year=[]
    for data in Income.objects.filter().values('date__year'):
        income_year.append(data['date__year'])                     
                
    expense_year=[]
    for data in Expenses.objects.filter().values('date__year'):
        expense_year.append(data['date__year'])  
    
    total_year=list(set(income_year+expense_year))
    
    month = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=total_month)
    year = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=total_year)

        
        
