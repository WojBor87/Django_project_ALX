from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from devboard.models import Project, Task
from devboard.forms import TaskForm


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'devboard/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count('tasks'))
            .order_by('-task_count')
        )


class ProjectDataView(LoginRequiredMixin, DetailView):
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


class TaskCreateView(LoginRequiredMixin, CreateView):
    '''
    Mój widok
    '''
    model = Task
    template_name = 'devboard/task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy("devboard:project_list")
    context_object_name = 'task'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, f"Zadanie '{form.instance.title}' zostalo dodane")
        return super().form_valid(form)

