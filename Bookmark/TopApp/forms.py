from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import AddBookmark,AddFolder
from django.contrib.auth.forms import AuthenticationForm,UsernameField
from django.utils.translation import ugettext_lazy as _
class SignUp(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label='Re-Password',widget=forms.PasswordInput(attrs={'placeholder':'Re-password'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {
            'email':'Email'
        }
        widgets = {
            "username": forms.TextInput(attrs={'placeholder':'username'}),
            "first_name": forms.TextInput(attrs={'placeholder':'first name','required':'required'}),
            "last_name": forms.TextInput(attrs={'placeholder':'last name','required':'required'}),
             "email": forms.EmailInput(attrs={'placeholder':'email','required':'required'}),
            }

class AddBookmarkForm(forms.ModelForm):
    class Meta:
        model = AddBookmark
        fields=['bookmarkLabel','bookmarkUrl']


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = AddFolder
        fields=['folderName','public']
        

class AuthenticationFormLogin(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'class','auto-focus':True,'placeholder':'username'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'class','placeholder':'password'}))
