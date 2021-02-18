from django.forms import ModelForm
from .models import Expenses, Category
from django import forms


class DateInput(forms.DateInput):
    input_type='date'

class ExpensesForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}))
    costs = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Costs'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}))
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'form-control', "type": "date"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ExpensesForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset= Category.objects.filter(user_id=user))

    class Meta:
        model = Expenses
        fields = ['title', 'costs', 'description', 'date', 'category']

class FilterForm(forms.Form):
    from_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'id':'from_month','class':'form-control', "type": "text",'placeholder':'From Date',"onfocus":"(this.type='date')","onblur":"(this.type='text')","onChange":"datefilter.submit();",'value':''}))
    to_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'id':'to_month','class':'form-control', "type": "text", 'placeholder': 'To Date',"onfocus": "(this.type='date')","onblur":"(this.type='text')","onChange":"datefilter.submit();",'value':''}))


