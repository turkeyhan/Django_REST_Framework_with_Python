from django.urls import path
from . import views
# Register your models here.

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
]