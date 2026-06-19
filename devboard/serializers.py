from rest_framework import serializers

from devboard.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, source='author.username')

    class Meta:
        model = Comment
        fields = ["id", "author_name", "body", "created_at"]
        read_only_fields = ["id", "created_at"]


