from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q, Count

from my_app.models import Task, SubTask, Category
from my_app.serializers.tasks import TaskSerializer, TaskCreateSerializer
from my_app.serializers.subtasks import SubTaskSerializer, SubTaskCreateSerializer
from my_app.serializers.categories import CategorySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['POST'])
def create_task(request: Request) -> Response:

    serializer = TaskSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_all_tasks(request: Request) -> Response:

    page_size = request.query_params.get('page_size')

    task_status = request.query_params.get('status')
    deadline = request.query_params.get('deadline')

    if task_status is None and deadline is None:

        tasks: Task = Task.objects.all()

    elif task_status is None and deadline is not None:
        tasks: Task = Task.objects.filter(deadline=deadline)

    elif task_status is not None and deadline is None:
        tasks: Task = Task.objects.filter(status=task_status)

    else:
        tasks: Task = Task.objects.filter(Q(status=task_status) & Q(deadline=deadline))

    if not tasks.exists():

        return Response(
            data=[],
            status=status.HTTP_204_NO_CONTENT
        )

    if page_size:
        try:
            paginator = Paginator(tasks, 5)
            tasks_per_page = paginator.page(page_size)
            serializer = TaskSerializer(tasks_per_page, many=True)
        except PageNotAnInteger as err:
            return Response(data=str(err), status=status.HTTP_200_OK)
        except EmptyPage as err:
            return Response(data=str(err), status=status.HTTP_204_NO_CONTENT)
    else:
        serializer = TaskSerializer(tasks, many=True)

    return Response(data=serializer.data, status=status.HTTP_200_OK)


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


class SubTaskListCreateView(APIView):

    def get(self, request: Request) -> Response:
        subtasks = SubTask.objects.all()
        if not subtasks.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self, pk: int) -> SubTask:
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk=pk)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, pk: int) -> Response:
        subtask = self.get_object(pk=pk)
        subtask.delete()

        return Response(
            data={
                'message': f'Deleted subtask {subtask.id}'
            },
            status=status.HTTP_200_OK
        )
