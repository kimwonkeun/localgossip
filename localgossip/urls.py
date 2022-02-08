"""localgossip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from local import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/<str:userid>/<str:tokenid>/<str:gpsX>/<str:gpsY>/<str:address>',views.login,name='login'),
    path('map/<str:gpsX>/<str:gpsY>',views.index,name='index'),
    path('addr/<str:address>',views.addr,name='addr'),
    path('inputmemo/<str:userid>/<str:gpsX>/<str:gpsY>',views.inputmemo,name="inputmemo"),
    path('savememo',views.savememo,name='savememo'),
    path('showmemo/<int:pk>/<str:userid>',views.showmemo,name='showmemo'),
    path('local/<str:address>/<str:uid>',views.local,name='local'),
    path('savequestion/<int:pk>/<str:questiondata>/<str:userid>',views.savequestion),    
    path('personallist/<str:userid>',views.myList,name='mylist'),
    path('status/<str:userid>',views.statusperson),
    path('saveperson',views.saveperson,name='saveperson'),
    path('userStatus/<str:userid>',views.homeStatus),
    path('showanswer/<int:pk>',views.showAnswer),
    path('saveAnswer/<int:pk>/<str:answer_data>',views.saveAnswer),
]
