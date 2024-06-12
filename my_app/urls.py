from django.urls import path
from .views import create_task, get_all_tasks, get_statistics


urlpatterns = [
    path('create/', create_task),
    path('get_all/', get_all_tasks),
    path('get_statistics/', get_statistics)
]
