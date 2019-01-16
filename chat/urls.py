from django.urls import path
from chat import views
app_name = 'chat';

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('reg/',views.reg,name='reg'),
    path('refresh/',views.reFresh,name='refresh'),
    path('sendmsg/',views.sendMsg,name='sendmsg'),
    path('getMsg/',views.getMsg,name='getMsg')
]