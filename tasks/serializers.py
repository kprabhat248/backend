from rest_framework import serializers
from .models import Task, TaskSubmission
from users.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    class Meta: model = Task; fields = '__all__'

class TaskSubmissionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    class Meta: model = TaskSubmission; fields = '__all__'