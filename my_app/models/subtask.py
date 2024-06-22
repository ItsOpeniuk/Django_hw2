from django.db import models

from my_app.contants.task_choices import TASK_STATUS_CHOICES
from my_app.models.task import Task


class SubTask(models.Model):
    title = models.CharField(max_length=50, verbose_name='Title.')
    description = models.TextField(null=True, blank=True, verbose_name='Description.')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='subtasks',
                             verbose_name='tasks',
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
