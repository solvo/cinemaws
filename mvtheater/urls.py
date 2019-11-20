from django.urls import path, include, re_path
from rest_framework import routers

from mvtheater.generic_views import Clients_rest_view, Movies_rest_view, Cinemas_rest_view, \
    Matinees_rest_view, Tickets_rest_view,   User_list
from mvtheater.views import Moviedetails_rest_view, annotate_view, aggregate_view, Billboard_rest_view
from mvtheater.views import Rest_get_object, aggregate_view2

router = routers.DefaultRouter()
router.register('clients', Clients_rest_view)
router.register('movies', Movies_rest_view)
router.register('cinemas', Cinemas_rest_view)
router.register('matinees', Matinees_rest_view)
router.register('tickets', Tickets_rest_view)
router.register('billboard', Billboard_rest_view)


urlpatterns = [
    path('rest/', include(router.urls)),
    path('rest/users/', User_list.as_view()),
    path('rest/movies/details/<str:pk>/', Moviedetails_rest_view.as_view()),
    path('rest/test/<int:pk>/', Rest_get_object.as_view()),
    path('rest/movies/details/<str:pk>/', Moviedetails_rest_view.as_view(), name='movdet'),
    path('rest/annotate/', annotate_view, name='annotate'),
    re_path(r'rest/aggregate/(?P<datein>\d{4}-\d{2}-\d{2})/(?P<dateend>\d{4}-\d{2}-\d{2})$', aggregate_view, name='aggregate'),
    re_path(r'rest/aggregate2/(?P<datein>\d{4}-\d{2}-\d{2})/(?P<dateend>\d{4}-\d{2}-\d{2})$', aggregate_view2),
]




