from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import (
    Topic,
    TopicQuery,
    ContentSource,
    DiscoveredContent,
    ContentEnrichment,
    PostCandidate,
    CrawlJob,
    FetchLog,
    ModerationLog,
)

@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'priority', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TopicQuery)
class TopicQueryAdmin(ModelAdmin):
    list_display = ('topic', 'query_text', 'is_active', 'lang_pref', 'weight')
    search_fields = ('query_text', 'topic__name')
    list_filter = ('is_active', 'lang_pref', 'topic')
    autocomplete_fields = ('topic',)


@admin.register(ContentSource)
class ContentSourceAdmin(ModelAdmin):
    list_display = ('name', 'source_type', 'is_active', 'reliability_score')
    search_fields = ('name', 'base_url', 'feed_url')
    list_filter = ('source_type', 'is_active')


@admin.register(DiscoveredContent)
class DiscoveredContentAdmin(ModelAdmin):
    list_display = ('title', 'source', 'topic', 'published_at', 'content_type', 'relevance_score', 'quality_score')
    search_fields = ('title', 'canonical_url', 'excerpt')
    list_filter = ('content_type', 'is_duplicate', 'language', 'source', 'topic')
    readonly_fields = ('url_hash', 'created_at')
    autocomplete_fields = ('source', 'topic', 'topic_query')
    date_hierarchy = 'published_at'


@admin.register(ContentEnrichment)
class ContentEnrichmentAdmin(ModelAdmin):
    list_display = ('content', 'created_at', 'confidence', 'read_time')
    search_fields = ('content__title', 'summary', 'simple_explanation')
    autocomplete_fields = ('content',)
    readonly_fields = ('created_at',)


@admin.register(PostCandidate)
class PostCandidateAdmin(ModelAdmin):
    list_display = ('__str__', 'platform', 'lang', 'status', 'intended_publish_time')
    search_fields = ('content__title', 'body_text')
    list_filter = ('status', 'platform', 'lang')
    autocomplete_fields = ('content', 'topics')
    date_hierarchy = 'intended_publish_time'
    list_select_related = ('content',)


@admin.register(CrawlJob)
class CrawlJobAdmin(ModelAdmin):
    list_display = ('run_date', 'status', 'findings_count', 'started_at', 'finished_at')
    search_fields = ('status', 'errors')
    list_filter = ('status', 'run_date')
    readonly_fields = ('run_date', 'started_at', 'finished_at', 'errors')


@admin.register(FetchLog)
class FetchLogAdmin(ModelAdmin):
    list_display = ('crawl_job', 'source', 'topic', 'status', 'items_found', 'started_at')
    search_fields = ('source__name', 'topic__name', 'request_signature')
    list_filter = ('status', 'source', 'topic')
    autocomplete_fields = ('crawl_job', 'topic', 'topic_query', 'source')
    readonly_fields = ('started_at', 'finished_at', 'error_detail')


@admin.register(ModerationLog)
class ModerationLogAdmin(ModelAdmin):
    list_display = ('post_candidate', 'status', 'created_at')
    search_fields = ('post_candidate__content__title', 'notes')
    list_filter = ('status',)
    autocomplete_fields = ('post_candidate',)
    readonly_fields = ('created_at',)