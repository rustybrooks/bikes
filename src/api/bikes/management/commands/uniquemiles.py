# from django.contrib.auth.models import User
# from django.core.management.base import BaseCommand, CommandError
#
# import bikes.models.season
# import bikes.models.strava_activity
# import bikes.models.strava_activity_stream
#
#
# class Path(object):
#     def __init__(self):
#         pass
#
#     def add(self, p1, p2):
#         return 0
#
#
# class PathSet(object):
#     def __init__(self):
#         self.paths = []
#
#     def add(self, p1, p2):
#         for p in self.paths:
#             if p.add(p1, p2):
#                 return
#
#         np = Path()
#         np.add(p1, p2)
#         self.paths.append(np)
#
#
# class Command(BaseCommand):
#     def add_arguments(self, parser):
#         pass
#         # parser.add_argument('poll_id', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         path = PathSet()
#
#         user = User.objects.filter(username="rbrooks").first()
#         seasons = bikes.models.activity.Season.objects.filter(user=user).order_by(
#             "-season_start_date"
#         )
#         season = seasons[0]
#
#         for activity in bikes.models.strava_activity.StravaActivity.objects.filter(
#             start_datetime_local__gte=season.season_start_date
#         ):
#             last = None
#             for foo in (
#                 bikes.models.strava_activity_stream.StravaActivityStream.objects.filter(
#                     activity=activity
#                 )
#             ):
#                 this = (foo.lat, foo.long)
#                 if last:
#                     path.add(last, this)
#
#                 last = this
#             break
#
#         print(path.paths)
