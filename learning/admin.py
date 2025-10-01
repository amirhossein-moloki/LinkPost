from django.contrib import admin
from .models import Topic, Chapter, Lesson

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'description')
    list_filter = ('topic',)
    search_fields = ('name', 'topic__name')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter')
    list_filter = ('chapter__topic', 'chapter')
    search_fields = ('name', 'chapter__name')