from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
import logging
import stravaapi
import withingsapi
from bikecal import models

logger = logging.getLogger(__name__)


def strava_connect(request):
    authorize_url = stravaapi.redirect_token()
    return HttpResponseRedirect(authorize_url)


def strava_callback(request):
    access_token = stravaapi.get_token(request.GET['code'], request.user)
    return HttpResponseRedirect(request.GET['state'])


@login_required
def strava_test(request):
    try:
        models.StravaActivity.sync_many(request.user)
        return redirect('calendar_index')
    except stravaapi.NoAuthCode:
        authorize_url = stravaapi.redirect_token(request.META['PATH_INFO'])
        return HttpResponseRedirect(authorize_url)


@login_required
def strava_update(request):
    try:
        import time
        t1 = time.time()
	updated = models.StravaActivity.update_curves()
        return HttpResponse("Yay %r %r" % (updated, time.time() - t1))
        return HttpResponse("Yay")

    except stravaapi.NoAuthCode:
        authorize_url = stravaapi.redirect_token(request.META['PATH_INFO'])
        return HttpResponseRedirect(authorize_url)


def withings_callback(request):
    logger.warn("withings_callback... post = %r", request.GET)

    w = withingsapi.WithingsClient(userid=request.GET['userid'])
    access_token = w.get_access_token(request.GET['oauth_verifier'])
    return HttpResponse("OK %r", access_token)


@login_required
def withings_test(request):
    try:
        w = withingsapi.WithingsClient()
        request_token = w.get_request_token('http://localhost:8000/withingscallback/')
        logger.warn("request token = %r", request_token)
        url = w.get_authorization_url(request_token)
        logger.warn("url = %r", url)
        return HttpResponseRedirect(url)

    except stravaapi.NoAuthCode:
        authorize_url = stravaapi.redirect_token(request.META['PATH_INFO'])
        return HttpResponseRedirect(authorize_url)
