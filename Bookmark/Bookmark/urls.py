from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

from django.conf import settings

from django.views.static import serve
import TopApp

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
      url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('',include('TopApp.urls')),
    path('accounts/', include('allauth.urls')),
    
    
]
handler404 = 'TopApp.views.error_404'