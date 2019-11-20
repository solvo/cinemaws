from django.contrib.auth.models import User
from django.db.models import Count, F, Q, Sum, FloatField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, status, permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from mvtheater.models import Movies, Cinemas, Matinees, Tickets

from mvtheater.pagination import Mamtinees_list_pagination
from mvtheater.serializers import User_serializer, Matinees_serializer
from mvtheater.utils import get_movie_details_from_api, check_for_matinees


class My_view(views.APIView, DjangoFilterBackend):   #OrderingFilter SearchFilter
    """
        This is the user list
    """

    queryset = None
    serializer_class = None
    pagination_class = None
    filterset_class = None
    # search_fields = ['username', 'first_name', 'last_name', ]
    # or filter_fields = ['username', 'first_name']
    # or ordering_fields = ['username', ]

    """
    filtros GET, cambie la linea por los comentarios para cambiar el tipo
    por busqueda, /?search=value.
    por variables, /?username__icontains=value&first_name__icontains=value&last_name__icontains=value 
    or /?username=value&first_name=value.
    Ordenar: ascendente -> ?ordering=username
             desecente -> ?ordering=-username
    """

    @property   # make it an object
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)  # returns pages list
                                                                                    # display page controls

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)  # returns JSON page controls

    def get_queryset(self, request):
        queryset = self.queryset
        queryset = self.filter_queryset(request, queryset, self)    # method from DjangoFilterBackend
        return queryset

    def get(self, request):
        user = self.get_queryset(request)
        page = self.paginate_queryset(user)

        if page is not None:
            serializer = User_serializer(page, many=True, context={'request': request})  # need the context for the hyperlink
            return self.get_paginated_response(serializer.data)  # Response(serializer.data)

        serializer = User_serializer(user, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = User_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Rest_get_object(views.APIView):
    queryset = User.objects.all()
    serializer_class = User_serializer
    """
    Retrieve, update or delete a user instance.
    """
    def get_queryset(self):
        queryset = self.queryset
        return queryset

    def get_object(self, pk):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)
        return obj

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = User_serializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = User_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Moviedetails_rest_view(views.APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request, pk):
        if pk != None:
            movie = get_object_or_404(Movies, id=pk)
            result = get_movie_details_from_api(movie.imdbid)
            return Response(result)
        return Response({'error':'No data found!'})

class Billboard_rest_view(ListAPIView, viewsets.ViewSet):
    lookup_url_kwarg = "date"
    serializer_class = Matinees_serializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = Mamtinees_list_pagination
    queryset = Matinees.objects.all()

    def get_queryset(self):
        uoption = self.request.query_params.get('date')
        if uoption != None:
            date_option = timezone.datetime.strptime(uoption,"%Y-%m-%d")
            matinees = check_for_matinees(date_option)
            return matinees
        matinees = check_for_matinees(timezone.now())
        return matinees


# ------------------------- Function Based Views -------------------------------
@api_view(['GET'])
def annotate_view(request):
    """
    :param request:
    :return: a list of cinemas and its matinees
    """
    result = Cinemas.objects.all().annotate(tanda_count=Count('matinees', filter=Q(matinees__cinema=F('id')))).values()
    response = list(result)
    return JsonResponse(response, safe=False)

@api_view(['GET'])
def aggregate_view(request, datein, dateend):
    """
    :param request:
    :return: a list of cinemas and its matinees
    """
    initial_date = parse_date(datein)
    final_date = parse_date(dateend)
    salas = Cinemas.objects.all().values('id', 'name')
    temp_dict = {}
    for sala in salas:
        temp_dict[sala['name'].replace(" ", "_")] = Sum('cost', filter=Q(cinema=sala['id']))
    date_filtered = Matinees.objects.all().filter(data_time__date__range=(initial_date, final_date))
    result = date_filtered.aggregate(**temp_dict)
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def aggregate_view2(request, datein, dateend):
    """
    :param request:
    :return: a list of cinemas and its matinees
    """
    initial_date = parse_date(datein)
    final_date = parse_date(dateend)
    costs = {}
    cinemas = Cinemas.objects.all()
    for cinema in cinemas:
        c = Tickets.objects.filter(matinee__data_time__range=(initial_date, final_date), matinee__cinema=cinema).count()
        costs[cinema.name.replace(" ", "_")] = Sum(F('matinees__cost')*c, filter=Q(matinees__cinema=cinema),
                                                   output_field=FloatField(), default=0.0)
    result = cinemas.aggregate(**costs)
    return JsonResponse(result, safe=False)
