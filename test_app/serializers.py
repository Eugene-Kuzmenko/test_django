from rest_framework import serializers
from test_app import models as app_models


class Item(serializers.ModelSerializer):

    class Meta:
        model = app_models.Item
        fields = ('name', 'type')
