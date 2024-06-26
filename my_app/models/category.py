from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)
