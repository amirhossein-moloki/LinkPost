from rest_framework import viewsets, views, status
from rest_framework.response import Response
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
    DraftBatch,
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
    DraftBatchCreateSerializer,
    DraftBatchApproveSerializer,
    DraftBatchReviseSerializer,
    AutomationLogCreateSerializer,
)

class DraftBatchCreateView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = DraftBatchCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DraftBatchApproveView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = DraftBatchApproveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        try:
            draft_batch = DraftBatch.objects.get(token=token)
        except DraftBatch.DoesNotExist:
            return Response({'error': 'DraftBatch not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Create Post objects
        campaign, _ = Campaign.objects.get_or_create(name='Default Campaign')
        platform, _ = Platform.objects.get_or_create(name='Default Platform')
        post_type, _ = PostType.objects.get_or_create(name='Text')
        status_obj, _ = PostStatus.objects.get_or_create(name='Approved', defaults={'order': 1})

        for post_data in draft_batch.posts:
            Post.objects.create(
                title=post_data['title'],
                body=post_data['body'],
                campaign=campaign,
                platform=platform,
                post_type=post_type,
                status=status_obj,
            )

        draft_batch.status = 'approved'
        draft_batch.save()

        # Mark lessons and chapter as processed
        draft_batch.lessons.update(processed=True)
        if not draft_batch.chapter.lessons.filter(processed=False).exists():
            draft_batch.chapter.processed = True
            draft_batch.chapter.save()

        return Response({'status': 'approved'}, status=status.HTTP_200_OK)


class DraftBatchReviseView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = DraftBatchReviseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['token']
        feedback = serializer.validated_data['feedback']
        try:
            draft_batch = DraftBatch.objects.get(token=token)
        except DraftBatch.DoesNotExist:
            return Response({'error': 'DraftBatch not found.'}, status=status.HTTP_404_NOT_FOUND)

        draft_batch.status = 'revised'
        draft_batch.feedback = feedback
        draft_batch.save()

        return Response({'status': 'revised'}, status=status.HTTP_200_OK)


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

    def get_serializer_class(self):
        if self.action == 'create':
            return AutomationLogCreateSerializer
        return AutomationLogSerializer
