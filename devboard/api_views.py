from rest_framework import viewsets, permissions

from devboard.models import Comment
from devboard.serializers import CommentSerializer

class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Comment.objects.filter(author=self.request.user)
            .select_related('author', 'task')
        )