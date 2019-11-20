from django.db.models import Count, F, Q, Sum
from django.http import JsonResponse

# Create your views here.
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view
from mvtheater.models import Cinemas, Matinees


# Create your views here.
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

