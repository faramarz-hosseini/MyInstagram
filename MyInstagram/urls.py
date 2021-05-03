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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from instagram import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.activity_feed, name='activity_feed'),
    path('search_result/', views.activity_feed, name='search_result'),
    path('login/', auth_views.LoginView.as_view(template_name='instagram/login_page.html'), name="login_page"),
    path('logout/', auth_views.LogoutView.as_view(template_name='instagram/logout_page.html'), name='logout_page'),
    path('new_password/', views.change_password, name='new_pass'),
    path('cv/', views.change_visibility, name='change_visibility'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('accept-follow/<str:user>', views.accept_follow_request, name='accept_follow'),
    path('decline-follow/<str:user>', views.decline_follow_request, name='decline-follow'),
    path('del-request/<str:username>', views.delete_follow_request, name='del-request'),
    path('register/', views.register, name='register'),
    path('new/', views.new_post, name='new_post'),
    path('notifications/', views.notification, name='notification'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('profile/<str:username>/follower', views.followers, name='followers'),
    path('profile/<str:username>/following', views.following, name='following'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
