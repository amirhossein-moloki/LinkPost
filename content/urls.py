from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CampaignViewSet,
    PlatformViewSet,
    PostTypeViewSet,
    PostStatusViewSet,
    TagViewSet,
    PostViewSet,
    PostTagViewSet,
    AttachmentViewSet,
    CommentViewSet,
    AutomationLogViewSet,
    DraftBatchCreateView,
    DraftBatchApproveView,
    DraftBatchReviseView,
)

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'platforms', PlatformViewSet)
router.register(r'post-types', PostTypeViewSet)
router.register(r'post-statuses', PostStatusViewSet)
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'post-tags', PostTagViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'automation-logs', AutomationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('drafts/', DraftBatchCreateView.as_view(), name='draft-batch-create'),
    path('approve/', DraftBatchApproveView.as_view(), name='draft-batch-approve'),
    path('revise/', DraftBatchReviseView.as_view(), name='draft-batch-revise'),
]
