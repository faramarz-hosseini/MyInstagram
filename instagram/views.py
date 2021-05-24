from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.utils import formats

from .forms import NewUserForm, NewPostForm, UserSearchForm, EditProfileForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from instagram.models import User, Posts, Profile, Follow, FollowRequest
from django.views import View

from itertools import chain
# Create your views here.


def activity_feed(request):
    if request.user.is_authenticated:
        return render(
            request,
            template_name='instagram/activity_feed.html',
            context={'title': 'Home!'}
        )
    else:
        return redirect('login_page')


def activity_feed_json(request, offset):
    querysets = Posts.objects.none()
    profile_pics = []
    results = {}
    entry = 1
    user_followed = Follow.objects.filter(follower=request.user)
    for obj in user_followed:
        user = User.objects.filter(username=obj.following).first()
        profile_pics.append(user.profile.profile_pic.url)
        posts_ = user.posts_set.all().order_by('-date_posted')[:5]
        querysets = querysets | posts_
    posts = querysets.order_by('-date_posted')[offset:offset+5]
    for post in posts:
        results[entry] = {
            'publisher': post.publisher.username,
            'post': post.picture.url,
            'caption': post.caption,
            'profile_pic': post.publisher.profile.profile_pic.url,
            'date_posted': formats.date_format(post.date_posted, "DATETIME_FORMAT"),
            'likes': post.likes
        }
        entry += 1

    return JsonResponse(results)


class SearchUsers(View):
    def post(self, request):
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

    def get(self, request):
        user_search_form = UserSearchForm(initial={'search_user': 'Enter Username...'})
        return render(request, "instagram/search_result.html", {'user_search_form': user_search_form})


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
    posts_num = Posts.objects.filter(publisher=user).count()
    profile_info = Profile.objects.filter(user=user).first()
    following = Follow.objects.filter(follower=user.id).count()
    followers = Follow.objects.filter(following=user.id).count()
    follow_record = Follow.objects.filter(follower=request.user.id, following=user.id).count()
    follow_request = FollowRequest.objects.filter(requester=request.user, requested=user).count()
    context = {'posts': posts,
               'posts_num': posts_num,
               'username': user,
               'profile_info': profile_info,
               'following': following,
               'followers': followers,
               'follow_record': follow_record,
               'follow_request': follow_request,
               }
    return render(request, template_name='instagram/profile.html', context=context)


class EditProfile(View):
    def post(self, request):
        _profile = Profile.objects.filter(user=request.user).first()
        edit_profile_form = EditProfileForm(request.POST, request.FILES, instance=_profile)
        if edit_profile_form.is_valid():
            edit_profile_form.save()
            messages.success(request, 'Changes are saved.')
        return redirect('profile', request.user.username)

    def get(self, request):
        edit_profile_form = EditProfileForm()
        return render(request, 'instagram/edit_profile.html', {'edit_profile_form': edit_profile_form})


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
    user = User.objects.filter(username=username).first()
    follower_id = request.user
    following_id = User.objects.filter(username=username).first()
    profile_info = Profile.objects.filter(user=user).first()
    if profile_info.is_public:
        follow_rec = Follow.objects.create(follower=follower_id, following=following_id)
        follow_rec.save()
        messages.info(request, f'You are now following {username}!')
    elif not profile_info.is_public:
        follow_request = FollowRequest.objects.create(requester=follower_id, requested=following_id)
        follow_request.save()
        messages.info(request, f'You requested to follow {username}.')
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
    follow_requests = FollowRequest.objects.filter(requested=request.user)
    context = {
        'follow_requests': follow_requests
    }
    return render(request, 'instagram/notification.html', context)


@login_required
def delete_follow_request(request, username):
    user_ = User.objects.filter(username=username).first()
    follow_request = FollowRequest.objects.filter(requester=request.user, requested=user_).first()
    follow_request.delete()
    messages.info(request, f"Your request to follow {username} was deleted.")
    return redirect('profile', username)


@login_required
def accept_follow_request(request, user):
    user_ = User.objects.filter(id=user).first()
    follow_request = FollowRequest.objects.filter(requester=user_, requested=request.user).first()
    follow_rec = Follow.objects.create(follower=user_, following=request.user)
    follow_request.delete()
    follow_rec.save()
    messages.info(request, f'{user_.username} is now following you.')
    return redirect('notification')


@login_required
def decline_follow_request(request, user):
    user_ = User.objects.filter(id=user).first()
    follow_request = FollowRequest.objects.filter(requester=user_, requested=request.user).first()
    follow_request.delete()
    messages.info(request, f"{user_.username}'s follow request was declined.")
    return redirect('notification')


def search_result_json(request, search):
    searched_user = User.objects.filter(username__contains=search)[:5]
    results = {}
    user_count = 1
    for user in searched_user:
        results[user_count] = {
            'username': user.username,
            'profile_pic': user.profile.profile_pic.url,
            'bio': user.profile.bio
        }
        user_count += 1

    return JsonResponse(results)
