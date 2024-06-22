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

    # @staticmethod
    # def check_name(name):
    #     """
    #     Check that the category name does not already exist.
    #     """
    #     if Category.objects.filter(name__iexact=name).exists():
    #         raise serializers.ValidationError('Sorry, this category already exists')
    #

    def validate_name(self, value):
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Sorry, this category already exists')

    # def create(self, validated_data):
    #     self.check_name(validated_data['name'])
    #     return super().create(validated_data)
    #
    # def update(self, instance, validated_data):
    #     if 'name' in validated_data:
    #         self.check_name(validated_data['name'])
    #     return super().update(instance, validated_data)
