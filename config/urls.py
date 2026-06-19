"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from devboard import urls as dev_urls
from devboard.api_views import (
    CommentViewSet, AllTaskViewSet, MyTaskViewSet,
    ProjectViewSet, ProjectWithTasksSet, ProjectWithEverythingSet
)

router = routers.DefaultRouter()
router.register("comments", CommentViewSet, basename="comment")
router.register("all_tasks", AllTaskViewSet, basename="all_task")
router.register("my_tasks", MyTaskViewSet, basename="my_task")
router.register("project", ProjectViewSet, basename="project")
router.register("project_tasks", ProjectWithTasksSet, basename="project_tasks")
router.register("project_tasks_comments", ProjectWithEverythingSet, basename="project_tasks_comments")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(dev_urls, namespace='devboard')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/v1/', include(router.urls)),
    path('api2/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api2/docs/', SpectacularSwaggerView.as_view(), name='docs'),
    path('api2/docs/redoc', SpectacularRedocView.as_view(), name='redoc'),
]

urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n"))
]