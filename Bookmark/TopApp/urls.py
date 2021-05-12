from django.urls import path
from . import views
urlpatterns = [
     path('',views.signInSignUp,name='signInSignUp'),
      path('mainPage/',views.mainPage,name="mainpage"),
      path('logout/',views.logout_function,name="logout"),
      path('changePassword/',views.changePassword,name="changepassword"),
      path('editprofile/',views.editProfile,name="editProfile"),
      path('addBookmark/',views.addBookMark,name='addBookmark'),
      path('bookmarks/<int:id>/',views.bookMarks,name='bookmarks'),
      path('deleteUrl/<int:id_folder>/<int:id_url>',views.deleteUrl,name='deleteUrl'),
      path('updateurl/<int:id_folder>/<int:id_url>/<str:label>/',views.updateUrl,name='updateurl'),
      path('deleteFolder/<int:id_folder>/',views.deleteFolder,name='deleteFolder'),


]
