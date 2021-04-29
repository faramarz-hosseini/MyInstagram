from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Posts(models.Model):
    picture = models.ImageField(upload_to='posts/')
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pictures/')
    bio = models.CharField(default='This user has not set a bio yet.', max_length=300)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='current_user', on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['follower', 'following']]

    def __str__(self):
        return f'{self.follower} is following {self.following}'

