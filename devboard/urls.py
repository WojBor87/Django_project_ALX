from django.urls import path
from devboard import views

app_name = "devboard"

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path("project/<int:pk>/", views.ProjectDataView.as_view(), name='project-details'),
]