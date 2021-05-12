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
        folder_name = AddFolder.objects.filter(public=True)
        # print(folder_name)
        folderNmme_url_dict = {}
        for foldername in folder_name:
            folderNm = foldername
            urls_name = AddBookmark.objects.filter(folderId=folderNm)
            folderNmme_url_dict[folderNm]=urls_name
            # print(foldername.folderName)
            # print(urls_name.ur)
        print(folderNmme_url_dict)
        for fn in folderNmme_url_dict:
            print("suman")
            print(folderNmme_url_dict.get(fn))
        # print(urls_name)
        # print(folder_name.user_token)

        return render(request,'html/mainPage.html',{"foldernameList":folderNmme_url_dict})
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

def addBookMark(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            folderForm = AddFolderForm(request.POST)
            if folderForm.is_valid():
                user_name = request.user
                fullname = request.user.get_full_name().capitalize()
                foldername = folderForm.cleaned_data['folderName']
                folderCreated = timezone.now()
                visibility = folderForm.cleaned_data['public']
                datas = AddFolder(user_token=user_name,userFullname=fullname,folderName=foldername,folderCreatedTime=folderCreated,public = visibility)
                datas.save()
        else:
            folderForm = AddFolderForm()
        fullname = request.user.get_full_name()
        urs = request.user.username
        # print(User.objects.filter(username=urs))
        name = AddFolder.objects.filter(user_token=request.user)
        return render(request,'html/addBookmark.html',{'folder':folderForm,'foldername':name})
    else:
        return HttpResponseRedirect('/login/')

def bookMarks(request,id):
    if request.user.is_authenticated:
        folderId_side = AddFolder.objects.filter(ids = id)
        folderId=''
        for particular in folderId_side:
            folderId = particular
            
        
        show_present_bookmarks = AddBookmark.objects.filter(folderId=folderId)
        if request.method == 'POST':
            urlForm = AddBookmarkForm(request.POST)
            if urlForm.is_valid():
                bookmarkLabel = urlForm.cleaned_data['bookmarkLabel']
                bookmarkUrl = urlForm.cleaned_data['bookmarkUrl']
                get_data = requests.get(bookmarkUrl)
                soup = BeautifulSoup(get_data.content,'html.parser')
                bookmarkTitle = soup.title.get_text()
                save_bookmark = AddBookmark(folderId=folderId,bookmarkLabel=bookmarkLabel,bookmarkUrl=bookmarkUrl,bookmarkTitle=bookmarkTitle)
                save_bookmark.save()
                urlForm =AddBookmarkForm()
        else:
            urlForm = AddBookmarkForm()
        return render (request,'html/bookmarks.html',{'id':id,'addUrls':urlForm,'showBookmarks':show_present_bookmarks})
    else:
        return HttpResponseRedirect('/')

def deleteUrl(request,id_folder,id_url):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delt = AddBookmark.objects.get(pk=id_url)
            delt.delete()
            redirect =  f'/bookmarks/{id_folder}/'
            return HttpResponseRedirect(redirect)
    else:
        return HttpResponseRedirect('/login/')

def updateUrl(request,id_folder,id_url,label):
    if request.user.is_authenticated:
        if request.method == 'POST':
            folder = AddFolder.objects.get(pk=id_folder)
            urlget = request.POST['urlgets']
            
            get_data = requests.get(urlget)
            soup = BeautifulSoup(get_data.content,'lxml')
            bookmarkTitle = soup.title.get_text()
            keys = AddBookmark(ids=id_url,folderId=folder,bookmarkLabel=label,bookmarkTitle=bookmarkTitle,bookmarkUrl=urlget)
            keys.save()
            
            updateForm = AddBookmarkForm()
            redirect =  f'/bookmarks/{id_folder}/'
            return HttpResponseRedirect(redirect)
    else:
        return HttpResponseRedirect('/login/')

def deleteFolder(request,id_folder):
    if request.user.is_authenticated:
        if request.method == 'POST':
            delt = AddFolder.objects.get(pk=id_folder)
            delt.delete()
            print("suman")
            print(id_folder)
            return HttpResponseRedirect("/addBookmark/")
    else:
        return HttpResponseRedirect("/login/")

def loginFunction(request):
    if not request.user.is_authenticated:
        if request.method == 'POST': 
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
        
        return render(request,"html/login.html",{'signIn':signIn})
    else:
        return HttpResponseRedirect("/")

def registerFunction(request):
    if not request.user.is_authenticated:
        return render(request,"html/register.html")
    else:
        return HttpResponseRedirect("/")


def main_user_view_function(request):
    if not request.user.is_authenticated:
        folder_name = AddFolder.objects.filter(public=True)
        # print(folder_name)
        folderNmme_url_dict = {}
        for foldername in folder_name:
            folderNm = foldername
            urls_name = AddBookmark.objects.filter(folderId=folderNm)
            folderNmme_url_dict[folderNm]=urls_name
            # print(foldername.folderName)
            # print(urls_name.ur)
        print(folderNmme_url_dict)
        for fn in folderNmme_url_dict:
            print("suman")
            print(folderNmme_url_dict.get(fn))
        # print(urls_name)
        # print(folder_name.user_token)

        return render(request,'html/user_view.html',{"foldernameList":folderNmme_url_dict})
    else:
        return HttpResponseRedirect('/')