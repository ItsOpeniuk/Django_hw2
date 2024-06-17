from django.utils import timezone
from rest_framework import serializers
from my_app.models import Task
from my_app.serializers.subtasks import SubTaskSerializer

class TaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = Task
        fields = '__all__'


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer()

    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline cannot be less than the current time")

        return value
