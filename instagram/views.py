from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpRequest
from django.shortcuts import render, redirect
from .forms import NewUserForm, NewPostForm, UserSearchForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from instagram.models import User, Posts, Profile, Follow

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
            user = User.objects.filter(username=user_name).first()
            user_profile = Profile.objects.create(user=user)
            user_profile.save()
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
    profile_info = Profile.objects.filter(user=user).first()
    following = Follow.objects.filter(follower=user.id).count()
    followers = Follow.objects.filter(following=user.id).count()
    follow_record = Follow.objects.filter(follower=request.user.id, following=user.id).count()
    context = {'posts': posts,
               'username': user,
               'profile_info': profile_info,
               'following': following,
               'followers': followers,
               'follow_record': follow_record,
               }
    return render(request, template_name='instagram/profile.html', context=context)


@login_required
def following(request, username):
    user = User.objects.filter(username=username).first()
    following_list = Follow.objects.filter(follower=user.id)
    followings = []
    for obj in following_list:
        followed_user = User.objects.filter(id=obj.following_id).first()
        followings.append(followed_user)
    context = {
        "followings": followings
    }
    return render(request, 'instagram/following.html', context)


@login_required
def followers(request, username):
    user = User.objects.filter(username=username).first()
    followers_list = Follow.objects.filter(following=user.id)
    followers = []
    for obj in followers_list:
        following_user = User.objects.filter(id=obj.follower_id).first()
        followers.append(following_user)
    context = {
        "followers": followers
    }
    return render(request, 'instagram/followers.html', context)


@login_required
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


@login_required
def change_visibility(request):
    profile_info = Profile.objects.filter(user=request.user).first()
    if profile_info.is_public:
        profile_info.is_public = False
        messages.success(request, 'Your profile visibility was successfully changed to private.')
    else:
        profile_info.is_public = True
        messages.success(request, 'Your profile visibility was successfully changed to public.')
    profile_info.save()
    return redirect('activity_feed')


@login_required
def follow(request, username):
    follower_id = request.user
    following_id = User.objects.filter(username=username).first()
    follow_rec = Follow.objects.create(follower=follower_id, following=following_id)
    follow_rec.save()
    messages.info(request, f'You successfully requested to follow {username}!')
    return redirect('profile', username)


@login_required
def unfollow(request, username):
    follower_id = request.user
    following_id = User.objects.filter(username=username).first()
    follow_rec = Follow.objects.filter(follower=follower_id, following=following_id).first()
    follow_rec.delete()
    messages.info(request, f'{username} was successfully unfollowed.')
    return redirect('profile', username)


@login_required
def notification(request):
    pass
