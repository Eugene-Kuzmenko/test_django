from django.test import TestCase, LiveServerTestCase, Client
from test_app import (
    views as app_views,
    viewsets as app_viewsets,
    models as app_models,
)
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import ParseError

requester = APIRequestFactory()


class ArraySortViewTestCase(TestCase):
    def assertErrorResponseCorrect(self, request, status_code, error_message):
        response = app_views.sort_array(request)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, error_message)

    def test_array_sorting(self):
        request = requester.post('/array-sort/', '[13, 32, 1, 2.5]', content_type='application/json')
        response = app_views.sort_array(request)

        self.assertEqual(response.data, [1, 2.5, 13, 32])

    def test_wrong_array(self):
        error_message = 'Incorrect data. Array elements should be numbers'
        self.assertErrorResponseCorrect(
            requester.post('/array-sort/', '["a", 24, 42, 41]', content_type='application/json'),
            400, error_message
        )
        self.assertErrorResponseCorrect(
            requester.post('/array-sort/', '[4, 24, {"a": 4}, 41]', content_type='application/json'),
            400, error_message
        )

    def test_should_not_be_string(self):
        error_message = 'Incorrect data. Should be array, not string'
        self.assertErrorResponseCorrect(
            requester.post('/array-sort/', '"savsrajiaskoksa"', content_type='application/json'),
            400, error_message
        )

    def test_should_not_be_object(self):
        error_message = 'Incorrect data. Should be array, not object'
        self.assertErrorResponseCorrect(
            requester.post('/array-sort/', '{ "a": 4, "b": "asd" }', content_type='application/json'),
            400, error_message
        )

    def test_parsing_error(self):
        request = requester.post('/array-sort/', '{ a: 4, "b": "asd" }', content_type='application/json')
        response = app_views.sort_array(request)
        self.assertRaises(ParseError)


def add_item(name, type):
    return app_models.Item.objects.create(name=name, type=type)


def add_ratio(recipe, item, qty, out=False):
    return app_models.RecipeItemAmount.objects.create(
        recipe_id=recipe,
        item_id=item,
        amount=qty,
        is_output=out,
    )


RECIPES_JSON = r"""
[
    {
        "id": 1,
        "name": "log to plank",
        "time": 1.0,
        "items": [
            {
                "id": 1,
                "item_id": 3,
                "recipe_id": 1,
                "name": "log",
                "amount": 1.0,
                "is_output": false,
                "type": "wood"
            },
            {
                "id": 2,
                "item_id": 2,
                "recipe_id": 1,
                "name": "plank",
                "amount": 4.0,
                "is_output": true,
                "type": "wood"
            }
        ]
    },
    {
        "id": 2,
        "name": "plank to stick",
        "time": 2.0,
        "items": [
            {
                "id": 3,
                "item_id": 2,
                "recipe_id": 2,
                "name": "plank",
                "amount": 2.0,
                "is_output": false,
                "type": "wood"
            },
            {
                "id": 4,
                "item_id": 1,
                "recipe_id": 2,
                "name": "stick",
                "amount": 4.0,
                "is_output": true,
                "type": "wood"
            }
        ]
    }
]
"""

ADDED_RECIPES_JSON = r"""
[
    {
        "id": 3,
        "name": "log to plank",
        "time": 1.0,
        "items": [
            {
                "id": 5,
                "item_id": 6,
                "recipe_id": 3,
                "name": "log",
                "amount": 1.0,
                "is_output": false,
                "type": "wood"
            },
            {
                "id": 6,
                "item_id": 5,
                "recipe_id": 3,
                "name": "plank",
                "amount": 4.0,
                "is_output": true,
                "type": "wood"
            }
        ]
    },
    {
        "id": 4,
        "name": "plank to stick",
        "time": 2.0,
        "items": [
            {
                "id": 3,
                "item_id": 5,
                "recipe_id": 4,
                "name": "plank",
                "amount": 2.0,
                "is_output": false,
                "type": "wood"
            },
            {
                "id": 4,
                "item_id": 6,
                "recipe_id": 4,
                "name": "stick",
                "amount": 4.0,
                "is_output": true,
                "type": "wood"
            }
        ]
    },
    {
        "id": 5,
        "name": "log to charcoal",
        "time": 2.5,
        "items": []
    }
]
"""


class RecipeTesting(LiveServerTestCase):
    def setUp(self):
        wood = app_models.ItemType.objects.create(name='wood')
        item1 = add_item('stick', wood)
        item2 = add_item('plank', wood)
        item3 = add_item('log', wood)
        recipe1 = app_models.Recipe.objects.create(name='log to plank', time=1)
        recipe2 = app_models.Recipe.objects.create(name='plank to stick', time=2)
        add_ratio(recipe1, item3, 1)
        add_ratio(recipe1, item2, 4, True)
        add_ratio(recipe2, item2, 2)
        add_ratio(recipe2, item1, 4, True)
        self.client = Client()

    def test_get_recipes(self):
        response = self.client.get('/recipes/')
        self.assertJSONEqual(str(response.content, encoding='UTF-8'), RECIPES_JSON)

    def test_post_recipes(self):
        self.client.post('/recipes/', {'name': "log to charcoal", 'time': 2.5})
        recipe3 = app_models.Recipe.objects.get(pk=5)
        self.assertIsNotNone(recipe3, 'recipe wasn\'t added to the database')
        self.assertEqual(recipe3.name, 'log to charcoal', 'recipe name is incorrect')
        self.assertEqual(recipe3.time, 2.5, 'recipe time is incorrect')