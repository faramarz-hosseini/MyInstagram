"""MyInstagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path

from instagram import views
from instagram.views import RegisterView, NewPostView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.activity_feed, name='activity_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='instagram/login_page.html'), name="login_page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='instagram/logout_page.html'), name='logout_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('new/', login_required(NewPostView.as_view()), name='new_post'),
    path('new_password/', views.change_password, name='new_pass'),
    path('profile/<str:username>', views.profile, name='profile'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
