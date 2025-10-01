from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, ChapterViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
