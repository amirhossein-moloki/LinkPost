from django.db import models
from django.contrib.auth.models import User

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=255)  # LinkedIn, Instagram, etc.

    def __str__(self):
        return self.name

class PostType(models.Model):
    name = models.CharField(max_length=255)  # text, image, video, carousel
    description = models.TextField()

    def __str__(self):
        return self.name

class PostStatus(models.Model):
    name = models.CharField(max_length=255)  # draft, review, approved, scheduled, published
    order = models.IntegerField()  # The order to display in a Kanban board

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

from learning.models import Lesson
from github.models import ChangeItem

class Post(models.Model):
    change_item = models.ForeignKey(ChangeItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    post_type = models.ForeignKey(PostType, on_delete=models.CASCADE)
    status = models.ForeignKey(PostStatus, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    title = models.CharField(max_length=255)
    body = models.TextField()
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, through='PostTag')

    def __str__(self):
        return self.title

class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'tag')

class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.type} for post {self.post.id}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class AutomationLog(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='logs')
    ACTION_CHOICES = (
        ('publish', 'Publish'),
        ('retry', 'Retry'),
        ('notify', 'Notify'),
    )
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    message = models.TextField()
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.post.title} - {self.status}"