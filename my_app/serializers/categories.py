from rest_framework import serializers
from my_app.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')

    def check_name(self, validated_data):

        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError('Sorry, this category already exists')

        return validated_data

    def create(self, validated_data):
        self.check_name(validated_data['name'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            self.check_name(validated_data['name'])
        return super().update(instance, validated_data)
