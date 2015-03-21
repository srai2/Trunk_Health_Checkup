__author__ = 'sandeep'
from django.conf.urls import patterns, url, include
from APL_THC import views

urlpatterns = patterns('',

        url(r'^(?P<cluster>[a-z]+)/$', views.index, name='index'),
        url(r'^route_pattern/(?P<cluster>[a-z]+)/$', views.pattern, name='pattern_list'),
        url(r'^route_pattern/(?P<dial_digit>[0-9]+)/$', views.pattern, name='pattern_detail')

)
