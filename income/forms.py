from django.forms import ModelForm
from .models import Income
from django import forms


class IncomeForm(ModelForm):
    source = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Source'}))
    income = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Income'}))
    date = forms.DateField(widget=forms.widgets.DateInput(attrs={'class':'form-control', "type": "date"}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(IncomeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Income
        fields = ['source', 'income', 'date']
