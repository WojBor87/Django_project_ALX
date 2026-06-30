from django.urls import path
from devboard import views

app_name = "devboard"

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path("project/<int:pk>/", views.ProjectDataView.as_view(), name='project_details'),
    path("zadania/nowe/", views.TaskCreateView.as_view(), name='task_create'),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name='task_detail'),
    path("task/<int:pk>/komentarz/nowy/", views.AddNewCommentToTask.as_view(), name='comment_add'),
]