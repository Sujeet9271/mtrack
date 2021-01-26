from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username', 'readonly': 'readonly'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}))

    class Meta:
        model=User
        fields=('username','first_name','last_name', 'email')

class ProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}))
    work = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'work'}))

    class Meta:
        model = Profile
        fields=('address','work')




