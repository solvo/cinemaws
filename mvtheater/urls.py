from django.urls import path, re_path

from mvtheater.generic_views import User_list
from mvtheater.views import  annotate_view, aggregate_view

urlpatterns = [
    path('rest/users/', User_list.as_view()),
    path('rest/annotate/', annotate_view, name='annotate'),
    re_path(r'rest/aggregate/(?P<datein>\d{4}-\d{2}-\d{2})/(?P<dateend>\d{4}-\d{2}-\d{2})$', aggregate_view, name='aggregate'),
]


