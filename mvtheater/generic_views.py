from django.contrib.auth.models import User

from mvtheater.filters import User_filter
from mvtheater.serializers import User_serializer
from mvtheater.views import My_view


class User_list(My_view):
    queryset = User.objects.all()
    serializer_class = User_serializer
    filterset_class = User_filter

    def get_queryset(self, request):
        queryset = self.queryset.filter(id=request.user.id)
        return queryset
