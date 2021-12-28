"""Rides URLs"""

# django
from django.db import router
from django.urls import path
from django.urls.conf import include

# Django REST framework
from rest_framework.routers import DefaultRouter

# views
from .views import rides as ride_views


router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[-a-zA-z0-0_]+)/rides',ride_views.RideViewSet,basename='rides'
)

urlpatterns=[
    path('',include(router.urls))
]
