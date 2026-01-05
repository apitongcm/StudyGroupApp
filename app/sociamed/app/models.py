from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=280, blank=True)
    attachment = models.FileField(
        upload_to='tweets/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')
