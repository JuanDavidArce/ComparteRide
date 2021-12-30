"""Users Serializers"""
# Django
from django.contrib.auth import authenticate,password_validation
from django.core.validators import RegexValidator
from django.conf import settings


# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator


# Models
from cride.users.models import User,Profile


# Utilities
import jwt


# Serializers
from cride.users.serializers.profiles import ProfileModelSerializer


# Tasks
from cride.taskapp.tasks import send_confirmation_email


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer"""

    profile = ProfileModelSerializer(read_only=True)
    class Meta:
        """Meta class"""
        model=User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'profile'
            
        )


class UserSignUpSerializer(serializers.Serializer):
    """User SignUp serializer.
    Handle sign up dta validation and user/profile creation"""
    email =serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )


    # Phone number
    phone_regex =RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="phone number must be entered in the format +999999999, Up to 15 digits allowed"

    )

    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    # Password
    password = serializers.CharField(min_length=8,max_length=64)
    password_confirmation = serializers.CharField(min_length=8,max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2,max_length=30)
    last_name = serializers.CharField(min_length=2,max_length=30)


    def validate(self,data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('Passwords do not math')
        password_validation.validate_password(passwd)
        return data


    def create(self,data):
        """Handle user and prifile creation"""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data,is_verified=False,is_client=True)
        Profile.objects.create(user=user)
        send_confirmation_email.delay(user_pk=user.pk)
        return user

    
   

class UserLoginSerializer(serializers.Serializer):
    """User Login serializer.
    Handle the login request data"""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8,max_length=64)


    def validate(self,data):
        """Check credentials"""
        user= authenticate(username=data['email'],password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user']=user
        return data


    def create(self,data):
        """Generate or retrieve new token"""
        token,created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'],token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer"""
    token = serializers.CharField()


    def validate_token(self,data):
        """Verify token is valid"""

        try:
            payload =  jwt.decode(data,settings.SECRET_KEY,algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')

        if payload['type']!= 'email_confirmation':
            raise serializers.ValidationError('Invalid Token')

        self.context['payload']=payload
        return data


    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()

