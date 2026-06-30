from django.urls import path
from devboard import views

app_name = "devboard"

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path("project/<int:pk>/", views.ProjectDetailView.as_view(), name='project_details'),
    path("projekty/nowy/", views.ProjectCreateView.as_view(), name="project-create"),
    path("zadania/nowe/", views.TaskCreateView.as_view(), name='task_create'),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name='task_detail'),
    path("task/<int:pk>/komentarz/nowy/", views.AddNewCommentToTask.as_view(), name='comment_add'),
]