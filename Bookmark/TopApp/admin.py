from django.contrib import admin
from . models import AddFolder,AddBookmark
# Register your models here.
@admin.register(AddFolder)
class AdminFolder(admin.ModelAdmin):
    list_display = ['ids','folderName','folderCreatedTime','public']

@admin.register(AddBookmark)
class AdminAddBookmark(admin.ModelAdmin):
    list_display = ['bookmarkLabel','bookmarkUrl']