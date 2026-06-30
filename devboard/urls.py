from django.urls import path
from devboard import views

app_name = "devboard"

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path("projekty/<int:pk>/", views.ProjectDetailView.as_view(), name='project_details'),
    path("projekty/nowy/", views.ProjectCreateView.as_view(), name="project-create"),
    path("zadania/nowe/", views.TaskCreateView.as_view(), name='task_create'),
    path("zadania/<int:pk>/", views.TaskDetailView.as_view(), name='task_detail'),
    path("zadania/<int:pk>/komentarz/nowy/", views.AddNewCommentToTask.as_view(), name='comment_add'),
    path("zadania/<int:pk>/edytuj/", views.TaskUpdateView.as_view(), name='task_update'),
    path("zadania/<int:pk>/usun/", views.TaskDeleteView.as_view(), name='task_delete'),
]