from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import NewUserForm, NewPostForm, UserSearchForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from instagram.models import Posts
from instagram.models import User

# Create your views here.


def activity_feed(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_search_form = UserSearchForm(request.POST)
            if user_search_form.is_valid():
                matched_users = User.objects.filter(username__icontains=user_search_form.cleaned_data.get("search_user"))
                context = {
                    "matched_users": matched_users,
                    "user_search_form": user_search_form,
                }

                if not matched_users:
                    context['matched_users'] = 'No user was found!'

                return render(request, 'instagram/search_result.html', context)
        else:
            user_search_form = UserSearchForm(initial={'search_user': 'Enter Username...'})

        return render(
            request,
            template_name='instagram/activity_feed.html',
            context={'title': 'Home!', 'user_search_form': user_search_form}
        )
    else:
        return redirect('login_page')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            messages.success(request, f"An account was successfully created for {user_name}. Log in below.")
            return redirect('login_page')
    else:
        form = NewUserForm
    return render(request, template_name='instagram/register.html', context={'register_form': form})


def new_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            new_post_form = NewPostForm(request.POST, request.FILES)
            if new_post_form.is_valid():
                post = new_post_form.save(commit=False)
                post.publisher = request.user
                post.save()
                messages.success(request, "Your post was successfully published.")
                return redirect('activity_feed')
        else:
            new_post_form = NewPostForm
    else:
        return redirect('login_page')
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

