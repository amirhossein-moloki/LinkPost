from django.db import models
from django.utils.text import slugify

class Topic(models.Model):
    """Represents a subject area to search for, e.g., 'Python', 'Django'."""
    name = models.CharField(max_length=255, unique=True, help_text="Title of the topic (e.g., 'Python')")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(blank=True, null=True, help_text="A brief description of the topic.")
    priority = models.IntegerField(default=100, help_text="Crawl priority (lower is higher).")
    is_active = models.BooleanField(default=True, help_text="Whether this topic is currently being crawled.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class TopicQuery(models.Model):
    """Specific search queries associated with a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='queries')
    query_text = models.CharField(max_length=500, help_text="The search query string (keywords, operators).")
    filters = models.JSONField(blank=True, null=True, help_text="Structured filters (e.g., domains, languages).")
    recency_window = models.IntegerField(default=30, help_text="Desired recency in days (e.g., 30 for the last month).")
    lang_pref = models.CharField(max_length=10, default='en', help_text="Preferred content language (e.g., 'en', 'fa').")
    weight = models.FloatField(default=1.0, help_text="Weight of this query's influence on scoring.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic.name}: {self.query_text[:50]}"

    class Meta:
        verbose_name_plural = "Topic Queries"


class ContentSource(models.Model):
    """A source of content, like a blog, RSS feed, or API."""
    SOURCE_TYPES = [('RSS', 'RSS'), ('WEB', 'Website'), ('API', 'API'), ('SOCIAL', 'Social Media')]

    name = models.CharField(max_length=255, help_text="Name of the source (e.g., 'Django News').")
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    base_url = models.URLField(max_length=500, help_text="Main URL of the source.")
    feed_url = models.URLField(max_length=500, blank=True, null=True, help_text="URL for the RSS/Atom feed, if applicable.")
    reliability_score = models.FloatField(default=0.8, help_text="A score from 0.0 to 1.0 indicating source reliability.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class DiscoveredContent(models.Model):
    """Raw, normalized content discovered from a source."""
    CONTENT_TYPES = [
        ('ARTICLE', 'Article'), ('BLOG', 'Blog Post'), ('DOC', 'Documentation'),
        ('RELEASE', 'Release Notes'), ('TWEET', 'Tweet'), ('VIDEO', 'Video'), ('OTHER', 'Other')
    ]

    canonical_url = models.URLField(max_length=2048, unique=True, help_text="The unique, canonical URL for the content.")
    url_hash = models.CharField(max_length=64, unique=True, editable=False, help_text="SHA-256 hash of the canonical URL for indexing.")
    title = models.CharField(max_length=500)
    excerpt = models.TextField(blank=True, null=True, help_text="A short summary or excerpt.")
    published_at = models.DateTimeField(blank=True, null=True, help_text="Original publication date of the content.")

    source = models.ForeignKey(ContentSource, on_delete=models.SET_NULL, null=True, related_name='discoveries')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, help_text="The primary topic this content was discovered for.")
    topic_query = models.ForeignKey(TopicQuery, on_delete=models.SET_NULL, null=True, help_text="The specific query that found this content.")

    language = models.CharField(max_length=10, blank=True, null=True)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES, default='ARTICLE')

    relevance_score = models.FloatField(default=0.0, help_text="Score of relevance to the query/topic.")
    quality_score = models.FloatField(default=0.0, help_text="Overall quality score based on various metrics.")
    is_duplicate = models.BooleanField(default=False)

    raw_payload = models.JSONField(blank=True, null=True, help_text="Raw data returned from the source API/scrape.")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.url_hash:
            import hashlib
            self.url_hash = hashlib.sha256(self.canonical_url.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name_plural = "Discovered Content"


class ContentEnrichment(models.Model):
    """Stores outputs from AI processing of discovered content."""
    content = models.OneToOneField(DiscoveredContent, on_delete=models.CASCADE, related_name='enrichment')
    summary = models.TextField(help_text="A concise summary of the content.")
    simple_explanation = models.TextField(help_text="'Explain Like I'm 5' style explanation.")
    key_points = models.JSONField(help_text="A list of key bullet points.")
    hashtags = models.JSONField(blank=True, null=True, help_text="A list of suggested hashtags.")
    read_time = models.IntegerField(blank=True, null=True, help_text="Estimated read time in minutes.")
    confidence = models.FloatField(blank=True, null=True, help_text="Model's confidence in the quality of the enrichment.")
    model_meta = models.JSONField(blank=True, null=True, help_text="Details about the model/prompt used.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enrichment for: {self.content.title[:50]}"

    class Meta:
        verbose_name_plural = "Content Enrichments"


class PostCandidate(models.Model):
    """A generated post draft, ready for review and publishing."""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'), ('APPROVED', 'Approved'), ('SCHEDULED', 'Scheduled'),
        ('PUBLISHED', 'Published'), ('REJECTED', 'Rejected'), ('FAILED', 'Failed')
    ]

    content = models.ForeignKey(DiscoveredContent, on_delete=models.CASCADE, related_name='candidates')
    topics = models.ManyToManyField(Topic, related_name='post_candidates')

    platform = models.CharField(max_length=50, help_text="Target platform (e.g., 'LinkedIn', 'X').")
    lang = models.CharField(max_length=10, default='en')
    tone = models.CharField(max_length=50, default='Professional')

    body_text = models.TextField(help_text="The suggested text for the post.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    intended_publish_time = models.DateTimeField(blank=True, null=True)
    external_post_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID of the post on the external platform.")

    meta = models.JSONField(blank=True, null=True, help_text="Additional metadata (e.g., CTA, UTM links).")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.platform} post for '{self.content.title[:50]}' ({self.status})"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Post Candidates"


class CrawlJob(models.Model):
    """Represents a single, daily execution of the content discovery pipeline."""
    STATUS_CHOICES = [
        ('QUEUED', 'Queued'), ('RUNNING', 'Running'), ('SUCCEEDED', 'Succeeded'),
        ('FAILED', 'Failed'), ('PARTIAL', 'Partial Success')
    ]

    run_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='QUEUED')

    topics_count = models.PositiveIntegerField(default=0)
    sources_count = models.PositiveIntegerField(default=0)
    queries_count = models.PositiveIntegerField(default=0)
    findings_count = models.PositiveIntegerField(default=0)

    errors = models.TextField(blank=True, null=True, help_text="Summary of errors encountered during the job.")
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Crawl Job for {self.run_date} ({self.status})"

    class Meta:
        ordering = ['-run_date']
        verbose_name_plural = "Crawl Jobs"


class FetchLog(models.Model):
    """Logs an individual fetch attempt from a content source."""
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'), ('RATE_LIMITED', 'Rate Limited'), ('ERROR', 'Error')
    ]

    crawl_job = models.ForeignKey(CrawlJob, on_delete=models.CASCADE, related_name='fetch_logs')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    topic_query = models.ForeignKey(TopicQuery, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(ContentSource, on_delete=models.CASCADE)

    request_signature = models.CharField(max_length=1024, help_text="A unique signature for the request (e.g., URL + params).")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    items_found = models.PositiveIntegerField(default=0)

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    error_detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.source.name} fetch at {self.started_at.strftime('%Y-%m-%d %H:%M')} - {self.status}"

    class Meta:
        ordering = ['-started_at']
        verbose_name_plural = "Fetch Logs"


class ModerationLog(models.Model):
    """Logs the moderation status and checks for a PostCandidate."""
    STATUS_CHOICES = [
        ('PASSED', 'Passed'), ('NEEDS_REVIEW', 'Needs Review'), ('REJECTED', 'Rejected')
    ]

    post_candidate = models.ForeignKey(PostCandidate, on_delete=models.CASCADE, related_name='moderation_logs')
    checks = models.JSONField(blank=True, null=True, help_text="Results of automated checks (e.g., length, keywords).")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NEEDS_REVIEW')
    notes = models.TextField(blank=True, null=True, help_text="Notes from the moderator or system.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Moderation for '{self.post_candidate.content.title[:30]}' - {self.status}"

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Moderation Logs"