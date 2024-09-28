from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from bikecal import models

class Command(BaseCommand):


    def add_arguments(self, parser):
        pass
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        user = User.objects.filter(username='rbrooks').first()
        seasons = models.Season.objects.filter(user=user).order_by('-season_start_date')
        season = seasons[0]

        f = open("/tmp/heatmap.dat", "w")
        for activity in models.StravaActivity.objects.filter(start_datetime_local__gte=season.season_start_date):
            for foo in models.StravaActivityStream.objects.filter(activity=activity):
                print >> f, foo.lat, foo.long
