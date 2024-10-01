# from bikecal import models
# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand, CommandError
#
# import bikes.models.season
# import bikes.models.strava_activity
# import bikes.models.strava_activity_stream
#
#
# class Command(BaseCommand):
#     def add_arguments(self, parser):
#         pass
#         # parser.add_argument('poll_id', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         user = User.objects.filter(username="rbrooks").first()
#         seasons = bikes.models.activity.Season.objects.filter(user=user).order_by(
#             "-season_start_date"
#         )
#         season = seasons[0]
#
#         f = open("/tmp/heatmap.dat", "w")
#         for activity in bikes.models.strava_activity.StravaActivity.objects.filter(
#             start_datetime_local__gte=season.season_start_date
#         ):
#             for foo in (
#                 bikes.models.strava_activity_stream.StravaActivityStream.objects.filter(
#                     activity=activity
#                 )
#             ):
#                 print >> f, foo.lat, foo.long
