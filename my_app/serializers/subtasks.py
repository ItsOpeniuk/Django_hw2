from rest_framework import serializers
from my_app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline')


class SubTaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline')
        read_only_fields = ['created_at']
