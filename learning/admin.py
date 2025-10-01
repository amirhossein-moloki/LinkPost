from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Topic, Chapter, Lesson

@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Chapter)
class ChapterAdmin(ModelAdmin):
    list_display = ('name', 'topic', 'description')
    list_filter = ('topic',)
    search_fields = ('name', 'topic__name')

@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ('name', 'chapter')
    list_filter = ('chapter__topic', 'chapter')
    search_fields = ('name', 'chapter__name')