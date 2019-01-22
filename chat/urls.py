from django.urls import path
from chat import views
app_name = 'chat';

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('reg/',views.reg,name='reg'),
    path('refresh/',views.reFresh,name='refresh'),
    path('sendMsg/',views.sendMsg,name='sendmsg'),
    path('getMsg/',views.getMsg,name='getMsg'),
    path('adduser/',views.addUser,name='addUser'),
]