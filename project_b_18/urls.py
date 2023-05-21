"""schedule_advisor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views, forms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html"), name='index'),
    
    path('accounts/signup/', views.signup_page, name='signup'),
    path('accounts/login/', views.login_page, name='login'),
    path('accounts/login/submit/', views.log_in, name='logged_in'),
    path('accounts/signup/submit/', views.signup, name='submit'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('search/', views.search_page, name='search'),
    path('edit/<int:strm>/<int:class_nbr>/', views.edit_schedule, name='edit_schedule'),

    path('schedule/', views.schedule_page, name='schedule'),
    path('schedule/send/', views.send_schedule, name='send_schedule'),
    path('advisor/schedules/', TemplateView.as_view(template_name="advisor_schedules.html"), name='advisor_schedules'),
    path('<str:uname>/schedule/', views.view_schedule_page, name='view_schedule'),
    path('<str:uname>/schedule/respond', views.respond_to_schedule, name='respond_to_schedule'),
]
