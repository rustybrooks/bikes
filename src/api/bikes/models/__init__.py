from .race import Race  # type: ignore
from .season import Season  # type: ignore
from .strava_activity import StravaActivity  # type: ignore
from .strava_activity_segment import (  # type: ignore
    StravaActivitySegmentEffort,
    StravaActivitySegmentEffortAch,
)
from .strava_activity_stream import StravaActivityStream  # type: ignore
from .strava_power_curve import StravaPowerCurve  # type: ignore
from .strava_segment import StravaSegment  # type: ignore
from .strava_segment_history import StravaSegmentHistory  # type: ignore
from .strava_segment_history_summary import StravaSegmentHistorySummary  # type: ignore
from .strava_speed_curve import StravaSpeedCurve  # type: ignore
from .strava_token import StravaToken  # type: ignore
from .training import TrainingEntry, TrainingWeek  # type: ignore

# This holds the user's particular schedule, to let them select things
# and move them around


# class Calendar:
#     def __init__(self, user=None, all=False):
#         self.user = user
#
#         self.season = list(
#             Season.objects.filter(user=self.user).order_by("season_start_date")
#         )[-1]
#         self.races = Race.objects.filter(season=self.season)
#
#         self.start_date = self.season.season_start_date
#         self.end_date = self.season.season_end_date
#
#         self.all = all
#
#         if all:
#             self.entries = self.season.entries()
#             self.workouts = self.season.workouts()
#         else:
#             self.select_start = tznow() - datetime.timedelta(weeks=2)
#             self.select_end = tznow() + datetime.timedelta(weeks=1)
#             self.entries = (
#                 TrainingEntry.objects.select_related("week")
#                 .select_related("season")
#                 .filter(
#                     week__week_start_date__range=(self.select_start, self.select_end)
#                 )
#             )
#
#             self.workouts = self.season.workouts(
#                 start_date=self.select_start, end_date=self.select_end
#             )
#
#     def weeks(self, week_start_date=None):
#         if week_start_date:
#             return (
#                 TrainingWeek.objects.select_related("season")
#                 .filter(week_start_date=week_start_date)
#                 .order_by("week_start_date")
#             )
#         elif self.all:
#             return (
#                 TrainingWeek.objects.select_related("season")
#                 .filter(season=self.season)
#                 .order_by("week_start_date")
#             )
#         else:
#             return (
#                 TrainingWeek.objects.select_related("season")
#                 .filter(week_start_date__range=(self.select_start, self.select_end))
#                 .order_by("week_start_date")
#             )
#
#     def entries_by_week(self, week):
#         m = {}
#         for d in range(7):
#             m[d] = []
#         for entry in [x for x in self.entries if x.week.id == week.id]:
#             diff = (entry.entry_date - week.week_start_date).days
#
#             try:
#                 m[diff].append(entry)
#             except KeyError:
#                 pass
#
#         return m.values()
#
#     def workouts_from_date(self, date):
#         return self.workouts[date]
#
#     def strava_workout_hours(self, week_start_date):
#         hours = 0
#         for day in range(7):
#             woday = week_start_date + datetime.timedelta(days=day)
#             hours += sum(
#                 [wo.moving_time / (60.0 * 60) for wo in self.workouts_from_date(woday)]
#             )
#
#         return hours
#
#     def strava_workouts(self, week_start_date):
#         wo = sum(
#             [
#                 self.workouts_from_date(week_start_date + datetime.timedelta(days=day))
#                 for day in range(7)
#             ],
#             [],
#         )
#         logger.warning("wo=%r", wo)
#         return wo
