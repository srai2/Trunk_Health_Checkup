__author__ = 'sandeep'
from django.conf.urls import patterns, url, include
from APL_THC import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
)
