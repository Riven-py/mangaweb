from django.contrib import admin
from django.urls import path
from sites.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('title/', open_title, name='titlepage'),
]
