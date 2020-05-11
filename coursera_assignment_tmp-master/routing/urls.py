from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    # url(r'index', views.index),
    # url(r'^.*$', views.index, name='index'),
    url(r'^simple_route\/*(?P<suffix>\w*)\/*$', views.simple_route),
    # url(r'^slug_route\\(?P<suffix>\w*)\\*$', views.slug_route),
    url(r'^slug_route\/*(?P<suffix>[^\/]*)\/*.*$', views.slug_route),
    url(r'^sum_route\/(?P<t1>-?\d+)\/(?P<t2>-?\d+)\/$', views.sum_route),
    url(r'^sum_get_method\/.*$', views.sum_get_method),
    url(r'^sum_post_method\/.*$', views.sum_post_method),
]
