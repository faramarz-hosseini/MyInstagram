from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Posts(models.Model):
    picture = models.ImageField(upload_to='posts')
    caption = models.TextField()
    likes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

