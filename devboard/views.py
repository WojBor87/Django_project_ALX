from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.views.generic import ListView, DetailView

from devboard.models import Project


class ProjectListView(ListView, LoginRequiredMixin):
    model = Project
    template_name = 'devboard/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        try:
            return (
                Project.objects.filter(owner=self.request.user)
                .annotate(task_count=Count('tasks'))
                .order_by('-task_count')
            )
        except TypeError:
            return None


class ProjectDataView(DetailView, LoginRequiredMixin):
    model = Project
    template_name = 'devboard/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = (
            self.object.tasks
            .select_related('assignee')
            .order_by('-priority', 'due_date')
        )
        return ctx
