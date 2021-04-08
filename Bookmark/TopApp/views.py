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
from .forms import AuthenticationFormLogin,PasswordChangeFormUser
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
                signIn = AuthenticationFormLogin(request=request,data=request.POST)
                if signIn.is_valid():
                    urss = signIn.cleaned_data['username']
                    pwdd = signIn.cleaned_data['password']
                    user = authenticate(username=urss,password=pwdd)
                    if user is not None:
                        messages.success(request,"Login successfull")
                        login(request,user)
                        return HttpResponseRedirect('/mainPage/')
            else:
                signIn = AuthenticationFormLogin()
        else:
            signUp = SignUp()
            signIn = AuthenticationFormLogin()
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


def changePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            changePasswordForm = PasswordChangeFormUser(user=request.user,data= request.POST)
            if changePasswordForm.is_valid():
                changePasswordForm.save()
                messages.success(request,"Your password is changed successfully,")
                return HttpResponseRedirect('/')
                
        else:
            changePasswordForm = PasswordChangeFormUser(user=request.user)
        return render(request,'html/changePassword.html',{'passwordForm':changePasswordForm})
    else:
        return HttpResponseRedirect('/')

def editProfile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            change = UserChangeForm(instance = request.user,data=request.POST)
            if change.is_valid():
                change.save()
        else:
            change = UserChangeForm(instance = request.user)
        if request.user.is_active == 1:
            ac = 'active'
        else:
            ac = 'offline'
        return render(request,'html/editProfile.html',{'name':request.user.get_full_name,'profileChange':change,'joined_date':request.user.date_joined,'last_loggedIn':request.user.last_login,'active':ac})
    else:
        return HttpResponseRedirect('/')