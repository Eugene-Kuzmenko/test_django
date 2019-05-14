from rest_framework import serializers
from test_app import models as app_models


class ItemType(serializers.ModelSerializer):

    class Meta:
        model = app_models.ItemType
        fields = ('name',)


class Item(serializers.ModelSerializer):

    class Meta:
        model = app_models.Item
        fields = ('id', 'name', 'type')


class RecipeItemAmount(serializers.ModelSerializer):
    name = serializers.CharField(source='item_id.name', read_only=True)
    type = serializers.CharField(source='item_id.type.name', read_only=True)

    class Meta:
        model = app_models.RecipeItemAmount
        fields = ('id', 'item_id', 'recipe_id', 'name', 'amount', 'is_output', 'type')


class Recipe(serializers.ModelSerializer):
    items = RecipeItemAmount(many=True, read_only=True)

    class Meta:
        model = app_models.Recipe
        fields = ('id', 'name', 'time', 'items')
