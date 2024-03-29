from django.contrib.auth.models import User
from django import forms
from .models import Profile


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username', 'readonly': 'readonly'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email', 'readonly': 'readonly'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'first_name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'last_name'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False)
    address = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'address'}))
    work = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'work'}))

    class Meta:
        model = Profile
        fields = ('address', 'work','profile_pic')





