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
