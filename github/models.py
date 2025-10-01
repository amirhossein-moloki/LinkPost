from django.db import models

class Repository(models.Model):
    provider = models.CharField(max_length=50, default="github")
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=511, unique=True)
    is_private = models.BooleanField(default=False)
    default_branch = models.CharField(max_length=255)
    topics = models.JSONField(null=True, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = "Repositories"
        indexes = [
            models.Index(fields=['owner', 'name']),
        ]

class ChangeItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('commit', 'Commit'),
        ('pr', 'Pull Request'),
        ('issue', 'Issue'),
    ]
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='change_items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    source_item_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    url = models.URLField(max_length=1024)
    changed_at = models.DateTimeField()
    raw_payload = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_type} {self.source_item_id} for {self.repository.full_name}"

    class Meta:
        unique_together = ('repository', 'item_type', 'source_item_id')
        indexes = [
            models.Index(fields=['changed_at']),
            models.Index(fields=['item_type', 'changed_at']),
            models.Index(fields=['repository', 'changed_at']),
        ]

class WorkflowState(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key