from rest_framework import viewsets
from .models import Repository, ChangeItem, WorkflowState
from .serializers import RepositorySerializer, ChangeItemSerializer, WorkflowStateSerializer


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer


class ChangeItemViewSet(viewsets.ModelViewSet):
    queryset = ChangeItem.objects.all()
    serializer_class = ChangeItemSerializer


class WorkflowStateViewSet(viewsets.ModelViewSet):
    queryset = WorkflowState.objects.all()
    serializer_class = WorkflowStateSerializer