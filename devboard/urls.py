from django.urls import path
from devboard import views

urlpatterns = [
    path('', views.index, name='index'),
    path('http/', views.http, name='http'),
]