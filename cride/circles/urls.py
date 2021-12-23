"""Cirlces URLs"""

# django
from django.db import router
from django.urls import path
from django.urls.conf import include

# Django REST framework
from rest_framework.routers import DefaultRouter

# views
from .views import circles as circle_views

router = DefaultRouter()
router.register(r'circles',circle_views.CircleViewSet,basename='circles')

urlpatterns=[
    path('',include(router.urls))
]
