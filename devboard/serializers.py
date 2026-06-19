from rest_framework import serializers

from devboard.models import Comment, Task, Project


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, source='author.username')

    class Meta:
        model = Comment
        fields = ["id", "task", "author_name", "body", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    assignee_name = serializers.CharField(read_only=True, source='assignee.username')
    project_name = serializers.CharField(read_only=True, source='project.name')

    class Meta:
        model = Task
        fields = [
            'id',
            'assignee_name',
            'project',
            'project_name',
            'title',
            'description',
            'status',
            'priority',
            'created_at',
            'due_date',
        ]
        read_only_fields = ["id", "created_at"]


class TaskWithCommentsSerializer(TaskSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + ["comments"]


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(read_only=True, source='owner.username')

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'owner_name',
            'created_at',
        ]
        read_only_fields = ["id", "created_at"]


class ProjectWithTasksSerializer(ProjectSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['tasks']


class ProjectWithEverythingSerializer(ProjectSerializer):
    tasks = TaskWithCommentsSerializer(many=True, read_only=True)

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ["tasks"]