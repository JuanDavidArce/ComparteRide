"""Circles views"""
# Django
from django.http import JsonResponse

# Models
from cride.circles.models import Circle

def list_circles(request):
    """List circles """
    circles = Circle.objects.filter(is_public=True)
    data = [circle.name for circle in circles]

    return JsonResponse(data,safe=False)