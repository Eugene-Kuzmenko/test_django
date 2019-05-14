from rest_framework import viewsets
from test_app import (
    serializers as app_serializers,
    models as app_models
)


class Item(viewsets.ModelViewSet):
    queryset = app_models.Item.objects.all()
    serializer_class = app_serializers.Item


class ItemType(viewsets.ModelViewSet):
    queryset = app_models.ItemType.objects.all()
    serializer_class = app_serializers.ItemType


class RecipeItemAmount(viewsets.ModelViewSet):
    queryset = app_models.RecipeItemAmount.objects.all()
    serializer_class = app_serializers.RecipeItemAmount


class Recipe(viewsets.ModelViewSet):
    queryset = app_models.Recipe.objects.all()
    serializer_class = app_serializers.Recipe