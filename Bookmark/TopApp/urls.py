from django.urls import path
from . import views
urlpatterns = [
     path('',views.signInSignUp,name='signInSignUp'),
      path('mainPage/',views.mainPage,name="mainpage"),
      path('logout/',views.logout_function,name="logout"),
      path('changePassword/',views.changePassword,name="changepassword"),
]
