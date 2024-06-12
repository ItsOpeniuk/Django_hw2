from rest_framework import serializers
from my_app.models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:

        model = SubTask
        fields = ('id', 'title', 'description', 'status', 'deadline'
        )