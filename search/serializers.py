from rest_framework import serializers
from .models import (
    Topic, TopicQuery, ContentSource, DiscoveredContent, ContentEnrichment,
    PostCandidate, CrawlJob, FetchLog, ModerationLog
)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'
        ref_name = "SearchTopic"


class TopicQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicQuery
        fields = '__all__'


class ContentSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSource
        fields = '__all__'


class DiscoveredContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscoveredContent
        fields = '__all__'


class ContentEnrichmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentEnrichment
        fields = '__all__'


class PostCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCandidate
        fields = '__all__'


class CrawlJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlJob
        fields = '__all__'


class FetchLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FetchLog
        fields = '__all__'


class ModerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = '__all__'