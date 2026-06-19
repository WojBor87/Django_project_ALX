from rest_framework import viewsets, permissions

from devboard.models import Comment, Task, Project
from devboard.serializers import CommentSerializer, TaskSerializer, ProjectSerializer, ProjectWithTasksSerializer, \
    ProjectWithEverythingSerializer, TaskWithCommentsSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Comment.objects.filter(author=self.request.user)
            .select_related('author', 'task')
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AllTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.filter(project__owner=self.request.user)
            .select_related('assignee', 'project')
        )


class MyTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Task.objects.filter(assignee=self.request.user)
            .select_related('assignee', 'project')
        )

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
        )


class ProjectWithTasksSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectWithTasksSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .select_related('owner')
        )


class ProjectWithEverythingSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectWithEverythingSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .select_related('owner')
        )