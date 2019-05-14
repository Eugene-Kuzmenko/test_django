from rest_framework import viewsets
from test_app import (
    serializers as app_serializers,
    models as app_models
)


class Item(viewsets.ModelViewSet):
    queryset = app_models.Item.objects.all()
    serializer_class = app_serializers.Item

