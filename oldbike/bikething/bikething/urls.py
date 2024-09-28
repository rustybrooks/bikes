from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^calendar/', include('bikecal.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    url(r'^stravaconnect/$', views.strava_connect, name="strava_connect"),
    url(r'^stravacallback/$', views.strava_callback, name="strava_callback"),
    url(r'^stravatest/$', views.strava_test, name="strava_test"),
    url(r'^stravaupdate/$', views.strava_update, name="strava_update"),

    url(r'^withingstest/$', views.withings_test, name="withings_test"),
    url(r'^withingscallback/$', views.withings_callback, name="withings_callback"),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
