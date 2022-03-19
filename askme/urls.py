"""askme URL Configuration

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

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='index'),
    path('question/', views.question_page, name='question'),
    path('new-question', views.new_question_page, name='new-question'),
    path('tag/cpp', views.tag_page, name='tag'),
    path('sign-up', views.register_page, name='sign-up'),
    path('sign-in', views.login_page, name='sign-in'),
    path('settings', views.user_settings_page, name='settings'),
]
