from rest_framework import viewsets
from .models import (
    Campaign,
    Platform,
    PostType,
    PostStatus,
    Tag,
    Post,
    PostTag,
    Attachment,
    Comment,
    AutomationLog,
)
from .serializers import (
    CampaignSerializer,
    PlatformSerializer,
    PostTypeSerializer,
    PostStatusSerializer,
    TagSerializer,
    PostSerializer,
    PostTagSerializer,
    AttachmentSerializer,
    CommentSerializer,
    AutomationLogSerializer,
)

class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer

class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer

class PostTypeViewSet(viewsets.ModelViewSet):
    queryset = PostType.objects.all()
    serializer_class = PostTypeSerializer

class PostStatusViewSet(viewsets.ModelViewSet):
    queryset = PostStatus.objects.all()
    serializer_class = PostStatusSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostTagViewSet(viewsets.ModelViewSet):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class AutomationLogViewSet(viewsets.ModelViewSet):
    queryset = AutomationLog.objects.all()
    serializer_class = AutomationLogSerializer
