from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Repository, ChangeItem, WorkflowState

@admin.register(Repository)
class RepositoryAdmin(ModelAdmin):
    list_display = ('full_name', 'provider', 'last_synced_at')
    search_fields = ('full_name', 'owner', 'name')
    list_filter = ('provider',)

@admin.register(ChangeItem)
class ChangeItemAdmin(ModelAdmin):
    list_display = ('repository', 'item_type', 'source_item_id', 'title', 'changed_at', 'processed')
    list_filter = ('item_type', 'processed', 'repository')
    search_fields = ('title', 'summary', 'source_item_id')

@admin.register(WorkflowState)
class WorkflowStateAdmin(ModelAdmin):
    list_display = ('key', 'value', 'updated_at')
    search_fields = ('key',)