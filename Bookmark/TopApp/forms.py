from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import AddBookmark,AddFolder
class SignUp(UserCreationForm):
    password2 = forms.CharField(label='Re-Password',widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {
            'email':'Email'
        }

class AddBookmarkForm(forms.ModelForm):
    class Meta:
        model = AddBookmark
        fields=['bookmarkLabel','bookmarkUrl']


class AddFolderForm(forms.ModelForm):
    class Meta:
        model = AddFolder
        fields=['folderName','public']
        
