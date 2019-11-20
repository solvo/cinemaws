from dateutil import parser
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, filters, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListAPIView

from mvtheater.custom_auth import UserCustomAuthentication
from mvtheater.filters import User_filter
from mvtheater.models import Clients, Movies, Cinemas, Matinees, Tickets
from mvtheater.permissions import ReadOnly
from mvtheater.serializers import User_serializer, Clients_serializer, Movies_serializer, Cinemas_serializer, \
    Matinees_serializer, Tickets_serializer
from mvtheater.views import My_view


class User_list(My_view):
    permission_classes = (permissions.IsAuthenticated, ReadOnly)
    queryset = User.objects.all()
    serializer_class = User_serializer
    filterset_class = User_filter

    def get_queryset(self, request):
        queryset = self.queryset.filter(id=request.user.id)
        return queryset

class Users_rest_view(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User_serializer
    filterset_class = User_filter
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)


class Clients_rest_view(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = Clients_serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    @property
    def perm(self):
        _perm = (permissions.IsAuthenticated, )
        if not self.request.user.has_perm('mvtheater.add_clients'):
            _perm = (permissions.IsAuthenticated, ReadOnly, )
        return _perm

    permission_classes = perm

class Movies_rest_view(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = Movies_serializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', ]
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)


class Cinemas_rest_view(viewsets.ModelViewSet):
    queryset = Cinemas.objects.all()
    serializer_class = Cinemas_serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)


class Matinees_rest_view(viewsets.ModelViewSet):
    queryset = Matinees.objects.all()
    serializer_class = Matinees_serializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)


class Tickets_rest_view(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = Tickets_serializer
    authentication_classes = (UserCustomAuthentication, SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
