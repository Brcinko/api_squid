__author__ = 'brcinko'

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^acl_rules/(?P<pk>\d+)/$', views.acl_rule_detail, name='acl_rule_detail'),
                       url(r'^acl_rules/$', views.acl_rules_list, name='acl_rules_list'),
                       # http_access
                       url(r'^acl_list/$', views.acl_list, name='acl_list'),
                       url(r'^acl_list/(?P<pk>\d+)/$', views.acl_list_detail, name='acl_list_detail'),
                       # authentication
                       url(r'^authentication/$', views.authentication, name='authentication'),
                       url(r'^authentication_db/$', views.authentication_db, name='authentication_db'),
                       url(r'^authentication/(?P<pk>\d+)/$', views.authentication_detail, name='authentication_detail'),
                       url(r'^authentication_db/(?P<pk>\d+)/$', views.authentication_db_detail, name='authentication_db_detail'),
                       # reconfigure
                       url(r'^update_config/$', views.update_config, name='update_config'),
                       )
urlpatterns = format_suffix_patterns(urlpatterns)
