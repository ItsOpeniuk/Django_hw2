from django.db import models

# Модель Task:
# Описание: Задача для выполнения.
# Поля:
# title: Название задачи. Уникально для даты.
# description: Описание задачи.
# categories: Категории задачи. Многие ко многим.
# status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
# deadline: Дата и время дедлайн.
# created_at: Дата и время создания. Автоматическое заполнение.

TASK_STATUS_CHOICES = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
    ('No status', 'No status')
]


class Task(models.Model):
    title = models.CharField(max_length=255,
                             unique_for_date='deadline',
                             verbose_name='Имя задачи.'
                             )
    description = models.TextField(null=True, blank=True, verbose_name='Описание задачи')
    categories = models.ManyToManyField('Category', verbose_name='Kaтегория')
    status = models.CharField(max_length=20,
                              choices=TASK_STATUS_CHOICES,
                              default='No status',
                              verbose_name='Статус выполнения'
                              )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Дата дедлайна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задания')

    def __str__(self):
        return self.title


# Модель SubTask:
# Описание: Отдельная часть основной задачи (Task).
# Поля:
# title: Название подзадачи.
# description: Описание подзадачи.
# task: Основная задача. Один ко многим.
# status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
# deadline: Дата и время дедлайн.
# created_at: Дата и время создания. Автоматическое заполнение.

class SubTask(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название подзадачи')
    description = models.TextField(null=True, blank=True, verbose_name='Описание подзадачи')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='subtask',
                             verbose_name='Задача',
                             null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=TASK_STATUS_CHOICES,
                              default='No status',
                              verbose_name='Статус выполнения'
                              )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Дата дедлайна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания задания')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.name
