from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.utils.translation import gettext_lazy as _

from devboard.models import Project, Task, Comment
from devboard.forms import TaskForm, CommentForm


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
        messages.success(self.request, _(f"Zadanie '{form.instance.title}' zostalo dodane"))
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'devboard/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = (
            self.object.comments
            .select_related('task')
            .order_by('-created_at', 'author')
        )
        return ctx


class AddNewCommentToTask(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'devboard/comment_add.html'
    form_class = CommentForm
    context_object_name = 'comment'

    def get_task(self):
        return Task.objects.filter(project__owner=self.request.user).get(pk=self.kwargs["pk"])

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["task"].queryset = self.get_queryset()
        task = self.get_task()
        form.initial["task"] = task
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("devboard:project_details", kwargs={"pk": self.object.task.project_id})

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["task"] = self.get_task()
        return ctx
