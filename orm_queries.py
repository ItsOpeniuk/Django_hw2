import os
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from django.utils import timezone
from datetime import timedelta
from my_app.models import Task, SubTask
from django.db.models import Q, F


def main():

    # Создание записей:

    # Task.objects.create(
    #     title="Prepare presentation",
    #     description="Prepare materials and slides for the presentation",
    #     status="New",
    #     deadline = timezone.now() + timedelta(days=3)
    # )


    # создание подзадач

    # new_task = Task.objects.get(title="Prepare presentation")
    #
    # subtasks = SubTask(
    #     title="Gather information",
    #     description="Find necessary information for the presentation",
    #     status="New",
    #     deadline=timezone.now() + timedelta(days=2),
    #     task=new_task
    # ),
    # SubTask(
    #     title="Create slides",
    #     description="Create presentation slides",
    #     status="New",
    #     deadline=timezone.now() + timedelta(days=2),
    #     task=new_task
    # )
    #
    # SubTask.objects.bulk_create(subtasks)

    # вывод данных

    # new_tasks = Task.objects.filter(status='new')
    # for task in new_tasks:
    #     print(f'{task.title} - {task.deadline}')


    # done_subtasks = SubTask.objects.filter(Q(status='DONE') & Q(deadline__lt=timezone.now()))
    # for subtask in done_subtasks:
    #     print(subtask)

    # try:
    #     my_task = Task.objects.get(title__exact='Prepare presentation')
    #     my_task.status = 'In progress'
    #     my_task.save()
    # except ObjectDoesNotExist:
    #     print('Task not found')

    # try:
    #     subtask = SubTask.objects.get(title="Gather information")
    #     subtask.deadline -= timedelta(days=2)
    #     subtask.save()
    # except ObjectDoesNotExist:
    #     print("No subtask found")

    subtask = SubTask.objects.get(title__exact='Create slides')
    subtask.title = "Create and format presentation slides"
    subtask.save()

    # 4. Удаление записей:
    # - Удалите задачу "Prepare presentation" и все ее подзадачи.
    Task.objects.get(title="Prepare presentation").delete()

if __name__ == '__main__':
    main()
