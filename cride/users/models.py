"""User model"""
#django

from django.db  import models
from django.contrib.auth.models import AbstractBaseUser

#Utilities
from cride.utils.models import CRideModel

class User(CRideModel,AbstractBaseUser):
    """User model 
    Extend from djangos's abstract user, change the username field, 
    to email and add some extra fields """
    email = models.EmailField(
        'email_address',
        unique=True,
        error_messages={
            'unique':'A user with that email already exists'
        }
    )

    phone_number = models.CharField(max_length=17,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['username','first_name','last_name']

    is_client=models.BooleanField(
        'client status',
        default=True,
        help_text=(
            'Help easili distinguish user and perform queries'
            'clients are the main type of user'
        )
    )
    
    is_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='set to true when the user have verified its email address'

    )

