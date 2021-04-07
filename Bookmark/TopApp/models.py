from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
# Create your models here.
class AddFolder(models.Model):
    ids=models.AutoField(primary_key=True)
    user_token = models.ForeignKey(User,on_delete=models.CASCADE)
    userFullname = models.CharField(max_length=50)
    # folderCreatedTime = models.DateField(auto_now_add=True,auto_now=False)
    folderName = models.CharField(max_length=100,unique=True)
    folderCreatedTime = models.DateTimeField()
    public = models.BooleanField("public",default=True)

    

class AddBookmark(models.Model):
    ids=models.AutoField(primary_key=True)
    folderId = models.ForeignKey(AddFolder,on_delete=models.CASCADE)
    bookmarkLabel = models.CharField(max_length=100)
    bookmarkTitle = models.CharField(max_length =300)
    bookmarkUrl = models.URLField()
