from rest_framework import serializers
from .models import Repository, ChangeItem, WorkflowState


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'


class ChangeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeItem
        fields = '__all__'


class WorkflowStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowState
        fields = '__all__'