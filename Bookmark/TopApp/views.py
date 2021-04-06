from django.shortcuts import render
from .forms import SignUp,AddBookmarkForm,AddFolderForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from .models import AddBookmark,AddFolder
from datetime import datetime
from django.utils import timezone
from bs4 import BeautifulSoup
import requests

def signInSignUp(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            if request.POST.get('signup'):
                signUp = SignUp(request.POST)
                if signUp.is_valid():
                    messages.success(request,"Account is created successfully " + request.POST['first_name']+" "+request.POST['last_name'])
                    signUp.save()
                    return HttpResponseRedirect('/')
            else:
                signUp = SignUp()
               
             
            if request.POST.get('signin'): 
                signIn = AuthenticationForm(request=request,data=request.POST)
                if signIn.is_valid():
                    urss = signIn.cleaned_data['username']
                    pwdd = signIn.cleaned_data['password']
                    user = authenticate(username=urss,password=pwdd)
                    if user is not None:
                        messages.success(request,"Login successfull")
                        login(request,user)
                        return HttpResponseRedirect('/mainPage/')
            else:
                signIn = AuthenticationForm()
        else:
            signUp = SignUp()
            signIn = AuthenticationForm()
        return render (request,'html/SignUp_SignIn.html',{'signUp':signUp,'signIn':signIn})
    else:
        return HttpResponseRedirect('/mainPage/')


def mainPage(request):
    if request.user.is_authenticated:
        return render(request,'html/mainPage.html')
    else:
        return HttpResponseRedirect('/')


def logout_function(request):
    logout(request)
    return HttpResponseRedirect('/')

# def func2(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             signIn = AuthenticationForm(request=request,data=request.POST)
#             if signIn.is_valid():
#                 urss = signIn.cleaned_data['username']
#                 pwdd = signIn.cleaned_data['password']
#                 user = authenticate(username=urss,password=pwdd)
#                 if user is not None:
#                     messages.success(request,"Login successfull")
#                     login(request,user)
#                     return HttpResponseRedirect('/mainPage/')
#         else:
#             signIn = AuthenticationForm() 
#         return render (request,'html/core2.html',{'signIn':signIn})
#     else:
#         return HttpResponseRedirect('/mainPage/')


# def signInSignUp(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             signUp = SignUp(request.POST)
#             if signUp.is_valid():
#                 messages.success(request,"Account is created successfully " + request.POST['first_name']+" "+request.POST['last_name'])
#                 signUp.save()
#                 signUp = SignUp()   
#         else:
#             signUp = SignUp()
            
#         return render (request,'html/SignUp_SignIn.html',{'signUp':signUp})
#     else:
#         return HttpResponseRedirect('/mainPage/')