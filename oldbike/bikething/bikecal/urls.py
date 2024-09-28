from django.conf.urls import patterns, url, include

from bikecal import views

urlpatterns = patterns('',
    url(r'^api/', include('bikecal.api.urls')),
    url(r'^$', views.index, name='calendar_index'),
    url(r'^r/$', views.index_react, name='calendar_index_react'),
    url(r'^summary/$', views.summary, name='calendar_summary'),
    url(r'^query/$', views.query, name='query'),
    url(r'^graph_cumulative/$', views.graph_cumulative, name='graph_cumulative'),
    url(r'^graph_weekly/$', views.graph_weekly, name='graph_weekly'),
    url(r'^graph_power/$', views.graph_power, name='graph_power'),
    url(r'^graph_power/(?P<rolling_window>\d+)$', views.graph_power, name='graph_power'),
    url(r'^graph_power/(?P<rolling_window>\d+)/(?P<interval_length>\d+)/$', views.graph_power, name='graph_power'),
    url(r'^(?P<entry_id>\d+)/$', views.update_entry, name='update_entry'),
    url(r'^reset_week/(?P<week_id>\d+)/$', views.reset_week, name='reset_week'),
    url(r'^activity/(?P<activity_id>\d+)$', views.activity, name='activity'),
    url(r'^activity/(?P<activity_id>\d+)/update$', views.activity_update, name='activity_update'),
    url(r'^activity/(?P<activity_id>\d+)/update_curves$', views.activity_update_curves, name='activity_update_curves'),
    url(r'^segment/(?P<segment_id>\d+)/$', views.segment, name='segment'),
    url(r'^reactest/', views.reactest, name='reactest'),
)
