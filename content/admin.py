from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Campaign,
    Platform,
    PostType,
    PostStatus,
    Tag,
    Post,
    PostTag,
    Attachment,
    Comment,
    AutomationLog,
)

@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Platform)
class PlatformAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PostType)
class PostTypeAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(PostStatus)
class PostStatusAdmin(ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ('title', 'campaign', 'platform', 'status', 'scheduled_at', 'published_at')
    list_filter = ('campaign', 'platform', 'status')
    search_fields = ('title', 'campaign__name')

@admin.register(PostTag)
class PostTagAdmin(ModelAdmin):
    list_display = ('post', 'tag')
    search_fields = ('post__title', 'tag__name')

@admin.register(Attachment)
class AttachmentAdmin(ModelAdmin):
    list_display = ('post', 'type', 'file')
    list_filter = ('type',)
    search_fields = ('post__title',)

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('post__title', 'author__username')

@admin.register(AutomationLog)
class AutomationLogAdmin(ModelAdmin):
    list_display = ('post', 'action', 'status', 'executed_at')
    list_filter = ('action', 'status')
    search_fields = ('post__title',)