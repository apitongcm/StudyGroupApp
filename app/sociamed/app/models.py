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

class Attachment(models.Model):
    post = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')

class Comment(models.Model):
    tweet = models.ForeignKey(
        'Tweet',
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'New Follower'),
        ('new_tweet', 'New Tweet'),
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    tweet = models.ForeignKey('Tweet', on_delete=models.CASCADE, null=True, blank=True) # Optional link to a tweet
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']