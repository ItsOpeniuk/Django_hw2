from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from my_app.views import (
    SubtaskListCreateGenericAPIView,
    SubtaskRetrieveUpdateDestroyAPIView,
    TaskDetailUpdateDeleteAPIView,
    CategoryViewSet,
    TaskListCreateGenericAPIView,
    get_statistics
)

router = DefaultRouter()
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('task_info/', get_statistics),
    path('tasks/', TaskListCreateGenericAPIView.as_view()),
    path('task/<int:pk>/', TaskDetailUpdateDeleteAPIView.as_view()),
    path('subtasks/', SubtaskListCreateGenericAPIView.as_view()),
    path('subtask/<int:pk>/', SubtaskRetrieveUpdateDestroyAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
