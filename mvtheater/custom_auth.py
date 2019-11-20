# my_app/authentication.py
import binascii

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
from rest_framework import exceptions
from base64 import standard_b64decode


class UserCustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_USERNAME')
        password = request.META.get('HTTP_PASSWORD')
        if not username:  # no username passed in request headers
            raise exceptions.AuthenticationFailed('Error 403: user was no given')  # authentication did not succeed
        try:
            user = User.objects.get(username=username)  # Check if right user was given
            if not check_password(standard_b64decode(password), user.password):  # Check if right password was given
                raise exceptions.AuthenticationFailed('Error 403: incorrect password')
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed('Error 403: the user %s was not found' % username)  # raise exception if user does not exist
        except binascii.Error:
            raise exceptions.AuthenticationFailed('Error 403: forbidden character in password, only Base64 chars supported')  # raise exception if user does not exist

        return user, None  # User authenticated
