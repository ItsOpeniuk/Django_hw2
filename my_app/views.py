from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, action
from rest_framework import status
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework_simplejwt.tokens import RefreshToken



from my_app.models import Task, SubTask, Category
from my_app.serializers.tasks import TaskSerializer, TaskCreateSerializer
from my_app.serializers.subtasks import SubTaskSerializer, SubTaskCreateSerializer
from my_app.serializers.categories import CategorySerializer, CategoryCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from my_app.serializers.user_serializer import UserRegistrationSerializer


class TaskListCreateGenericAPIView(ListCreateAPIView):


    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        return Task.objects.all()


class TaskDetailUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):


    __model = Task

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super(TaskDetailUpdateDeleteAPIView, self).get_permissions()

    def get_object(self):
        return get_object_or_404(queryset=self.__model, pk=self.kwargs['pk'])

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATH']:
            return TaskCreateSerializer
        return TaskSerializer


@api_view(['GET'])
def get_statistics(request: Request) -> Response:
    task_counter = Task.objects.aggregate(task_count=Count('id'))
    task_count_by_status = Task.objects.values('status').annotate(tasks_counter=Count('id')).order_by('status')
    failed_tasks = Task.objects.filter(deadline__lte=timezone.now())

    if task_counter['task_count'] > 0 or failed_tasks.exists():
        data = {
            'total_tasks': task_counter['task_count'],
            'tasks_by_status': list(task_count_by_status),
            'failed_tasks': TaskSerializer(failed_tasks, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)
    else:
        return Response(data=[], status=status.HTTP_204_NO_CONTENT)


class SubtaskListCreateGenericAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer


class SubtaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    __model = SubTask

    def get_permissions(self):

        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]

        else:
            self.permission_classes = [IsAdminUser]

        return super(SubtaskRetrieveUpdateDestroyAPIView, self).get_permissions()

    def get_object(self):
        return get_object_or_404(SubTask, pk=self.kwargs.get('pk'))

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return CategorySerializer

        return CategoryCreateSerializer

    @action(detail=False, methods=['get'], url_path='statistic')
    def count_tasks(self, request: Request) -> Response:

        count_task_for_category = Category.objects.annotate(tasks_count=Count('task'))
        data = [
            {'category': category.name,
             'tasks_count': category.tasks_count
             }
            for category in count_task_for_category
        ]

        return Response(data)
