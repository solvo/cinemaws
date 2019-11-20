from django.contrib.auth.models import User
from django_filters.rest_framework import FilterSet


class User_filter(FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['icontains'],
            'first_name': ['icontains'],
            'last_name': ['icontains'],
        }