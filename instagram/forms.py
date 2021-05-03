from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Posts, Profile


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['picture', 'caption']


class UserSearchForm(forms.Form):
    search_user = forms.CharField(label="", max_length=100)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        labels = {
            "profile_pic": 'Profile picture',
            "bio": 'Bio',
            "is_public": 'Public profile'
        }
        fields = ['profile_pic', 'bio', 'is_public']
