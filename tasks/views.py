from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskSubmission
from .serializers import TaskSerializer, TaskSubmissionSerializer
from .permissions import IsAdminOrReadOnly

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def submit_task(self, request, pk=None):
        if TaskSubmission.objects.filter(task_id=pk, user=request.user).exists():
            return Response({'error': 'You have already submitted for this task.'}, status=status.HTTP_400_BAD_REQUEST)
        submission = TaskSubmission.objects.create(task_id=pk, user=request.user, screenshot=request.data.get('screenshot'))
        return Response(TaskSubmissionSerializer(submission).data, status=status.HTTP_201_CREATED)

class SubmissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return TaskSubmission.objects.filter(user=self.request.user) if not self.request.user.is_staff else TaskSubmission.objects.all()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        sub = self.get_object()
        if sub.status != 'APPROVED':
            sub.status = 'APPROVED'; sub.save()
            sub.user.points += sub.task.points; sub.user.save()
        return Response(TaskSubmissionSerializer(sub).data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        sub = self.get_object(); sub.status = 'REJECTED'; sub.save()
        return Response(TaskSubmissionSerializer(sub).data)