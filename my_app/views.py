from django.utils import timezone
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q, Count

from my_app.models import Task, SubTask, Category
from my_app.serializers.tasks import TaskSerializer
from my_app.serializers.subtasks import SubTaskSerializer
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

        return Response(data=[], status=status.HTTP_204_NO_CONTENT)

    if page_size:
        try:
            paginator = Paginator(tasks, 5)
            tasks_per_page = paginator.page(page_size)
            serializer = TaskSerializer(tasks_per_page, many=True)
        except PageNotAnInteger as err:
            return Response(data=str(err), status=status.HTTP_200_OK)
        except EmptyPage as err:
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)
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