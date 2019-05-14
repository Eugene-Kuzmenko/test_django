from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Item(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL)


class Recipe(models.Model):
    name = models.CharField(max_length=50)
    time = models.FloatField(default=0)


class Ammount(models.Model):
    recipe_id = models.ForeignKey(to=Recipe, related_name='items', on_delete=models.CASCADE)
    item_id = models.ForeignKey(to=Item, on_delete=models.CASCADE)
    is_output = models.BooleanField(default=False)

# Create your models here.
