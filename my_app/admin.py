from django.contrib import admin
from my_app.models import Task, SubTask, Category

# Register your models here.
class SubTaskInline(admin.StackedInline):
    model = SubTask
    can_delete = True
    verbose_name_plural = 'Subtasks'
    extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title',)
    list_filter = ('category', )
    ordering = ('-created_at',)
    inlines = [SubTaskInline]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'created_at')
    search_fields = ('title', 'status')




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
