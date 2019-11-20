from dateutil import parser
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.generics import ListAPIView


from mvtheater.filters import User_filter
from mvtheater.models import Clients, Movies, Cinemas, Matinees, Tickets
from mvtheater.serializers import User_serializer, Clients_serializer, Movies_serializer, Cinemas_serializer, \
    Matinees_serializer, Tickets_serializer
from mvtheater.views import My_view


class User_list(My_view):
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



class Clients_rest_view(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = Clients_serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]



class Movies_rest_view(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = Movies_serializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', ]



class Cinemas_rest_view(viewsets.ModelViewSet):
    queryset = Cinemas.objects.all()
    serializer_class = Cinemas_serializer


class Matinees_rest_view(viewsets.ModelViewSet):
    queryset = Matinees.objects.all()
    serializer_class = Matinees_serializer



class Tickets_rest_view(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = Tickets_serializer

class Billboard_rest_view(ListAPIView, viewsets.ViewSet):
    lookup_url_kwarg = "date"
    serializer_class = Matinees_serializer
    queryset = Matinees.objects.all()
    #renderer_classes = [JSONRenderer]
    filterset_fields = ['data_time']

    def get_queryset(self):

        querydate = timezone.now().date()
        uoption = self.request.query_params.get('date')
        if uoption != None:
            try:
                newdate = parser.parse(uoption)
                if newdate:
                    querydate=newdate.date()
            except ValueError as e:
                pass
            except OverflowError as eo:
                pass

        return Matinees.objects.filter(data_time__date=querydate)
