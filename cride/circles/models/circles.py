"""Circle model"""
# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel


class Circle(CRideModel):
    """Circle model
    A circle is a private group where riedes are affered and taken 
    by its members. to join a circle a user must recive an unique 
    invitation code from an existing circle member"""


    name = models.CharField('circle name',max_length=140)
    slug_name = models.SlugField(unique=True,max_length=40)

    about = models.CharField('circle description',max_length=255)
    picture = models.ImageField(upload_to='circles/pictures',blank=True,null=True)
    


    # Stats
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken= models.PositiveIntegerField(default=0)

    members = models.ManyToManyField('users.User',through='circles.Membership',through_fields=('circle','user'))

    verified = models.BooleanField(
        'verified circle',
        default=False,
        help_text='Verigied circles are also known as official communities'
    )

    is_public = models.BooleanField(
        default=True,
        help_text='Public circels are listed in the main page so everyone know about their existence'
    )

    is_limited = models.BooleanField(
        'limited',
        default=False,
        help_text='Limited ciercles can grow up to a fixed number of members'
    )

    members_limit = models.PositiveIntegerField(
        default=0,
        help_text='If circle is limited, this will be the limit on the number of members'
    )

    def __str__(self):
        
        """Return circel name"""
        return self.name

    class Meta(CRideModel.Meta):
        """Meta class"""
        ordering =['-rides_taken','-rides_offered']