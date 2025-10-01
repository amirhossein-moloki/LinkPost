from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TopicViewSet, TopicQueryViewSet, ContentSourceViewSet,
    DiscoveredContentViewSet, ContentEnrichmentViewSet, PostCandidateViewSet,
    CrawlJobViewSet, FetchLogViewSet, ModerationLogViewSet
)

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'topic-queries', TopicQueryViewSet)
router.register(r'content-sources', ContentSourceViewSet)
router.register(r'discovered-content', DiscoveredContentViewSet)
router.register(r'content-enrichments', ContentEnrichmentViewSet)
router.register(r'post-candidates', PostCandidateViewSet)
router.register(r'crawl-jobs', CrawlJobViewSet)
router.register(r'fetch-logs', FetchLogViewSet)
router.register(r'moderation-logs', ModerationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]