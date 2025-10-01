from rest_framework import viewsets
from .models import (
    Topic, TopicQuery, ContentSource, DiscoveredContent, ContentEnrichment,
    PostCandidate, CrawlJob, FetchLog, ModerationLog
)
from .serializers import (
    TopicSerializer, TopicQuerySerializer, ContentSourceSerializer,
    DiscoveredContentSerializer, ContentEnrichmentSerializer, PostCandidateSerializer,
    CrawlJobSerializer, FetchLogSerializer, ModerationLogSerializer
)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicQueryViewSet(viewsets.ModelViewSet):
    queryset = TopicQuery.objects.all()
    serializer_class = TopicQuerySerializer


class ContentSourceViewSet(viewsets.ModelViewSet):
    queryset = ContentSource.objects.all()
    serializer_class = ContentSourceSerializer


class DiscoveredContentViewSet(viewsets.ModelViewSet):
    queryset = DiscoveredContent.objects.all()
    serializer_class = DiscoveredContentSerializer


class ContentEnrichmentViewSet(viewsets.ModelViewSet):
    queryset = ContentEnrichment.objects.all()
    serializer_class = ContentEnrichmentSerializer


class PostCandidateViewSet(viewsets.ModelViewSet):
    queryset = PostCandidate.objects.all()
    serializer_class = PostCandidateSerializer


class CrawlJobViewSet(viewsets.ModelViewSet):
    queryset = CrawlJob.objects.all()
    serializer_class = CrawlJobSerializer


class FetchLogViewSet(viewsets.ModelViewSet):
    queryset = FetchLog.objects.all()
    serializer_class = FetchLogSerializer


class ModerationLogViewSet(viewsets.ModelViewSet):
    queryset = ModerationLog.objects.all()
    serializer_class = ModerationLogSerializer