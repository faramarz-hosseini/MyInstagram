from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View

from instagram.models import Posts
from instagram.models import User
from .forms import NewUserForm, NewPostForm


@login_required
def activity_feed(request):
    return render(request, template_name='instagram/activity_feed.html', context={'title': 'Home!'})


class RegisterView(View):
    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            messages.success(request, f"An account was successfully created for {user_name}. Log in below.")
            return redirect('login_page')

    def get(self, request):
        form = NewUserForm
        return render(request, template_name='instagram/register.html', context={'register_form': form})


class NewPostView(View):
    def post(self, request):
        new_post_form = NewPostForm(request.POST, request.FILES)
        if new_post_form.is_valid():
            post = new_post_form.save(commit=False)
            post.publisher = request.user
            post.save()
            messages.success(request, "Your post was successfully published.")
            return redirect('activity_feed')

    def get(self, request):
        new_post_form = NewPostForm
        return render(request, template_name='instagram/new_post.html', context={'new_post_form': new_post_form})


@login_required()
def profile(request, username):
    user = User.objects.filter(username=username).first()
    if user is None:
        return HttpResponseNotFound('<h1> This user does not exist.</h1>')
    posts = Posts.objects.filter(publisher=user)
    context = {'posts': posts,
               'username': user,
               }
    return render(request, template_name='instagram/profile.html', context=context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, template_name='instagram/new_password.html', context={'form': form})

