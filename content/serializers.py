from rest_framework import serializers
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

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = '__all__'

class PostStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostStatus
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = '__all__'

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AutomationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomationLog
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'change_item', 'campaign', 'platform', 'post_type', 'status',
            'lesson', 'title', 'body', 'scheduled_at', 'published_at',
            'created_at', 'updated_at', 'tags', 'campaign_name', 'platform_name',
            'status_name'
        ]
