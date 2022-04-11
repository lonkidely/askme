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
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.new_questions_page, name='new-questions'),
    path('hot-questions', views.hot_questions_page, name='hot-questions'),
    path('question/<int:number>/', views.question_page, name='question'),
    path('ask', views.new_question_page, name='new-question'),
    path('tag/<str:tag>/', views.tag_page, name='tag'),
    path('sign-up', views.register_page, name='sign-up'),
    path('login', views.login_page, name='sign-in'),
    path('settings', views.user_settings_page, name='settings'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.not_found_page
