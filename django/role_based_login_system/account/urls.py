from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('student/', views.student, name='student'),
    path('employee/', views.employee, name='employee'),
    path('complaint_form/', views.complaint_form, name='complaint_form'),
    path('complaint_list/', views.complaint_list, name='complaint_list'),
   
]