from django.urls import path
from .views import create_task, get_all_tasks, get_statistics
from my_app.views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView

urlpatterns = [
    path('create/', create_task),
    path('get_all/', get_all_tasks),
    path('get_statistics/', get_statistics),
    path('subtasks/', SubTaskListCreateView.as_view()),
    path('subtasks/<int:pk>', SubTaskDetailUpdateDeleteView.as_view())
]
