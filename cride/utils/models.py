"""Django models utilities"""
from django.db import models

class CRideModel(models.Model):
    """Comparte Ride base model"""


    """CrideModel acts as an abstract base class from which every 
    other model in the porject will inherit. This class provides
    every table with the following atributes:
    +created(DateTime): Store the datetime the object was created
    +modified(DateTme):Store the last datetime the object was modified """


    created = models.DateTimeField('created_at',auto_now_add=True,help_text='Date time on which the object was last modified')
    modified = models.DateTimeField('modified_at',auto_now=True,help_text='Date time on which the object was last modified')

    class Meta:
        """Meta option"""
        abstract =True
        get_latest_by ='created'
        ordering = ['-created','-modified']