from django.contrib import admin
from django.urls import path, include
from dashboard import views

urlpatterns = [
   
    path('',views.dashboard,name='dashboard'),
    path('test',views.test,name='test'),
    
  
]