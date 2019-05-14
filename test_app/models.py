from django.db import models


class ItemType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    class Meta:
        db_table = 'item_type'


class Item(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(to=ItemType, on_delete=models.SET_NULL, null=True)


class Recipe(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    time = models.FloatField(default=0)


class Amount(models.Model):
    recipe_id = models.ForeignKey(to=Recipe, related_name='items', on_delete=models.CASCADE)
    item_id = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    is_output = models.BooleanField(default=False)

