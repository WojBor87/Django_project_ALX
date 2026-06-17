from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView

from devboard.models import Project


class ProjectListView(ListView,LoginRequiredMixin):
    model = Project
    template_name = 'devboard/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count('tasks'))
            .order_by('-task_count')
        )

