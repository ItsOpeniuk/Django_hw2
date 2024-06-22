from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskListGenericAPIView, get_statistics
from my_app.views import (
    SubtaskListGenericAPIView,
    SubtaskRetrieveUpdateDestroyAPIView,
    TaskCreateUpdateDeleteAPIView,
    CategoryViewSet
)

router = DefaultRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('task_info/', get_statistics),
    path('tasks/', TaskListGenericAPIView.as_view()),
    path('task/<int:pk>/', TaskCreateUpdateDeleteAPIView.as_view()),
    path('subtasks/', SubtaskListGenericAPIView.as_view()),
    path('subtask/<int:pk>/', SubtaskRetrieveUpdateDestroyAPIView.as_view())
]
