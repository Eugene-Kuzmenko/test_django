"""TestProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from test_app import (
    viewsets as test_app_viewsets,
    views as test_app_views
)

router = routers.SimpleRouter()

router.register(r'items', test_app_viewsets.Item)
router.register(r'types', test_app_viewsets.ItemType)
router.register(r'recipes', test_app_viewsets.Recipe)
router.register(r'recipe-items', test_app_viewsets.RecipeItemAmount)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sort-array/', test_app_views.sort_array)
]

urlpatterns += router.urls
