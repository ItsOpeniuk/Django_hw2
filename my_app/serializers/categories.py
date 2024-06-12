from rest_framework import serializers
from my_app.models import Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category
        fields = ('id', 'name')