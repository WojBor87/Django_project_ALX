from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.utils.translation import gettext_lazy as _

from devboard.mixins import OwnerQuerySetMixin
from devboard.models import Project, Task, Comment
from devboard.forms import TaskForm, CommentForm, ProjectForm


class ProjectListView(OwnerQuerySetMixin, ListView):
    model = Project
    template_name = 'devboard/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return (
            super().get_queryset()
            .annotate(task_count=Count('tasks'))
            .order_by('-task_count')
        )


class ProjectDetailView(OwnerQuerySetMixin, DetailView):
    model = Project
    template_name = 'devboard/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tasks'] = (
            self.object.tasks
            .select_related('assignee')
            .order_by('-priority', 'due_date')
        )
        return ctx


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "devboard/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("devboard:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Projekt '{form.instance.name}' został utworzony.")
        return super().form_valid(form)


class TaskCreateView(LoginRequiredMixin, CreateView):
    '''
    Mój widok
    '''
    model = Task
    template_name = 'devboard/task_create.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse(Task.project.get_absolute_url)

    context_object_name = 'task'

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get("project")
        if project_id:
            initial["project"] = project_id
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, _(f"Zadanie '{form.instance.title}' zostalo dodane"))
        return super().form_valid(form)


class TaskUpdateView(OwnerQuerySetMixin, UpdateView):
    model = Task
    template_name = 'devboard/task_create.html'
    form_class = TaskForm
    owner_field = "project__owner"

    def get_success_url(self):
        return reverse(Task.project.get_absolute_url)


class TaskDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Task
    owner_field = "project__owner"

    def get_success_url(self):
        return reverse(Task.project.get_absolute_url)


class TaskStatusView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        q_owner = Q(project__owner=self.request.user)
        q_assignee = Q(assignee=self.request.user)
        qs = Task.objects.filter(q_owner | q_assignee).filter(pk=self.kwargs["pk"])
        task = get_object_or_404(qs)
        new_status = request.POST.get("status")

        if not new_status or new_status not in Task.Status.values:
            raise BadRequest("Missing or incorrect status value")

        task.status = new_status
        task.save()

        messages.success(request, "Status zaktualizowany")
        return redirect(task.project.get_absolute_url)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'devboard/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = (
            self.object.comments
            .select_related('task')
            .order_by('-created_at', 'author')
        )
        return ctx


class TaskSearchView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "devboard/task_search.html"
    context_object_name = "tasks"

    def get_queryset(self):
        query = self.request.GET.get("q", "")

        queryset = Task.objects.filter(
            project__owner=self.request.user
        )

        # TODO: Dodać wyszukiwanie po kilku słowach rozdzielonych znakiem białym
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        return queryset.select_related("project", "assignee")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["query"] = self.request.GET.get("q", "")
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
        return reverse(Task.project.get_absolute_url)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["task"] = self.get_task()
        return ctx
