from django.db import models


TASK_STATUS_CHOICES = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
    ('No status', 'No status')
]


class Task(models.Model):
    title = models.CharField(max_length=50,
                             unique_for_date='deadline',
                             verbose_name='Title.'
                             )
    description = models.TextField(null=True, blank=True, verbose_name='Description.')
    category = models.ManyToManyField('Category', verbose_name='Category')
    status = models.CharField(max_length=20,
                              choices=TASK_STATUS_CHOICES,
                              default='No status',
                              verbose_name='Status'
                              )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Deadline')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        unique_together = ('title',)


class SubTask(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title.')
    description = models.TextField(null=True, blank=True, verbose_name='Description.')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='subtask',
                             verbose_name='Subtask',
                             null=True, blank=True)
    status = models.CharField(max_length=20,
                              choices=TASK_STATUS_CHOICES,
                              default='No status',
                              verbose_name='Status'
                              )
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Deadline')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created_at')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'Subtask'
        unique_together = ('title',)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)
