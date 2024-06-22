from django.utils import timezone
from rest_framework import serializers

from my_app.models import SubTask


class SubTaskShortDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'deadline')


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = SubTask
        fields = ('id', 'title', 'task', 'description', 'status', 'deadline')


class SubTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'task', 'description', 'status', 'deadline')
        read_only_fields = ['created_at']

    @staticmethod
    def validate_deadline(value):
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline cannot be less than the current time")

        return value
