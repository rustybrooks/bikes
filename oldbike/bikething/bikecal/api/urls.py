from django.conf.urls import patterns, url

from bikecal.api import views

urlpatterns = patterns('',
    url(r'^week/(?P<week_start_date>.+)/$', views.week, name='calendar_api_week'),
    url(r'^week_by_offset/(?P<week_offset>-?\d+)/$', views.week_by_offset, name='calendar_api_week_offset'),
    url(r'^move_entry/(?P<entry_id>-?\d+)/(?P<jsdate>-?\d+)/$', views.move_entry, name='calendar_api_move_entry'),
    url(r'^entry/(?P<entry_id>.+)/set_workout_type/(?P<workout_type>.+)/$', views.set_workout_type, name='calendar_api_set_workout_type'),
    url(r'^entry/(?P<entry_id>.+)/$', views.entry, name='calendar_api_entry'),
    url(r'^workout_summary/(?P<user_id>[^/]+)$', views.workout_summary, name='calendar_api_workout_summary'),
    url(r'^activity_streams/(?P<activity_id>[^/]+)$', views.activity_streams, name='calendar_api_workout_streams'),
    url(r'^activity_curves/(?P<activity_id>[^/]+)$', views.activity_curves, name='calendar_api_workout_curves'),
    url(r'^zones/(?P<user_id>[^/]+)$', views.zones, name='calendar_api_zones'),
    )
