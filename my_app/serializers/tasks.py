from django.utils import timezone
from rest_framework import serializers
from my_app.models import Task, Category, SubTask
from my_app.serializers.categories import CategorySerializer
from my_app.serializers.subtasks import SubTaskShortDetailSerializer


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskShortDetailSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    subtask = serializers.SlugRelatedField(
        slug_field='title', queryset=SubTask.objects.all(),
        many=True, required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'subtask', 'status', 'deadline']

    @staticmethod
    def validate_deadline(value):
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline cannot be less than the current time")

        return value

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtask')
        task = Task.objects.create(**validated_data)
        for subtask_title in subtasks_data:
            subtask = SubTask.objects.get(title=subtask_title)
            subtask.task = task
            subtask.save()
        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtask', [])
        instance = super().update(instance, validated_data)
        for subtask_title in subtasks_data:
            subtask = SubTask.objects.get(title=subtask_title)
            subtask.task = instance
            subtask.save()
        return instance

