from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Users
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UsersDetailsSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Users.EMAIL_FIELD

