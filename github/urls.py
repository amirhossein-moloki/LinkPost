from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepositoryViewSet, ChangeItemViewSet, WorkflowStateViewSet

router = DefaultRouter()
router.register(r'repositories', RepositoryViewSet)
router.register(r'change-items', ChangeItemViewSet)
router.register(r'workflow-states', WorkflowStateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]