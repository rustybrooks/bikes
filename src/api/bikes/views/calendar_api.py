# import calendar
# import datetime
# import logging
#
# import pytz  # type: ignore
# from api_framework import Api, api_datetime, api_register, HttpResponse  # type: ignore
# from flask import render_template
#
# from api.utils import is_logged_in  # type: ignore
# from bikedb import queries  # type: ignore
#
# logger = logging.getLogger(__name__)
#
#
# def format_interval(duration):
#     return str(datetime.timedelta(seconds=duration))
#
#
# @api_register(None, require_login=is_logged_in)
# class CalendarTemplateApi(Api):
#     @classmethod
#     def _fixdate(cls, d, tz):
#         return pytz.utc.localize(d).astimezone(tz)
#
#     @classmethod
#     def index(
#         cls, date=None, week_start_day=5, timezone="US/Central", _user=None
#     ):  # monday is 0, 5 is saturday etc
#         tz = pytz.timezone(timezone)
#         date = api_datetime(date) or cls._fixdate(datetime.datetime.utcnow(), tz)
#         logger.warning("date=%r", date)
#
#         cal = calendar.Calendar(week_start_day)
#         weeks = cal.monthdatescalendar(date.year, date.month)
#         first = weeks[0][0]
#         last = weeks[-1][-1]
#
#         first = tz.localize(
#             datetime.datetime(first.year, first.month, first.day)
#         ).astimezone(pytz.utc)
#         last = tz.localize(
#             datetime.datetime(last.year, last.month, last.day)
#         ).astimezone(pytz.utc)
#
#         # logger.warning("%r", cal.monthdatescalendar(date.year, date.month))
#         logger.warning(
#             "first=%r, last=%r",
#             first.astimezone(pytz.utc),
#             last.astimezone(pytz.utc) + datetime.timedelta(days=1),
#         )
#
#         activities = queries.activities(
#             user_id=_user.user_id,
#             start_datetime_after=first.astimezone(pytz.utc),
#             start_datetime_before=last.astimezone(pytz.utc)
#             + datetime.timedelta(days=1),
#         )
#         logger.warning("%r", activities[0])
#
#         data = {}
#         day_to_week = {}
#         week_index = 0
#         for w in weeks:
#             logger.warning("w = %r", w)
#             data["{}:totals".format(week_index)] = {
#                 "moving_time": 0,
#                 "distance_mi": 0,
#             }
#             for d in w:
#                 day_to_week[d] = week_index
#                 data[d] = {"activities": []}
#
#             week_index += 1
#
#         logger.warning("data keys = %r", data.keys())
#
#         for a in activities:
#             ad = cls._fixdate(a.start_datetime, tz).date()
#             # ad = a.start_datetime
#
#             logger.warning("%r - %r", ad, ad in data)
#             data[ad]["activities"].append(a)
#             data["{}:totals".format(day_to_week[ad])]["distance_mi"] += a.distance_mi
#             data["{}:totals".format(day_to_week[ad])]["moving_time"] += a.moving_time
#
#         return HttpResponse(
#             render_template(
#                 "calendar/index.html",
#                 weeks=weeks,
#                 data=data,
#                 day_to_week=day_to_week,
#                 format_interval=format_interval,
#             )
#         )
#
#
# @api_register(None, require_login=is_logged_in)
# class Calendar(Api):
#     @classmethod
#     def _fixdate(cls, d, tz):
#         return pytz.utc.localize(d).astimezone(tz)
#
#     @classmethod
#     def index(
#         cls, date=None, week_start_day=5, timezone="US/Central", _user=None
#     ):  # monday is 0, 5 is saturday etc
#         tz = pytz.timezone(timezone)
#         date = api_datetime(date) or cls._fixdate(datetime.datetime.utcnow(), tz)
#         logger.warning("date=%r", date)
#
#         cal = calendar.Calendar(week_start_day)
#         weeks = cal.monthdatescalendar(date.year, date.month)
#         first = weeks[0][0]
#         last = weeks[-1][-1]
#
#         first = tz.localize(
#             datetime.datetime(first.year, first.month, first.day)
#         ).astimezone(pytz.utc)
#         last = tz.localize(
#             datetime.datetime(last.year, last.month, last.day)
#         ).astimezone(pytz.utc)
#
#         # logger.warning("%r", cal.monthdatescalendar(date.year, date.month))
#         logger.warning(
#             "first=%r, last=%r",
#             first.astimezone(pytz.utc),
#             last.astimezone(pytz.utc) + datetime.timedelta(days=1),
#         )
#
#         activities = queries.activities(
#             user_id=_user.user_id,
#             start_datetime_after=first.astimezone(pytz.utc),
#             start_datetime_before=last.astimezone(pytz.utc)
#             + datetime.timedelta(days=1),
#         )
#         # logger.warning("%r", activities[0])
#
#         data = {}
#         day_to_week = {}
#         week_index = 0
#         for w in weeks:
#             logger.warning("w = %r", w)
#             for d in w:
#                 day_to_week[d] = week_index
#                 data[d.isoformat()] = {"activities": []}
#
#             week_index += 1
#
#         logger.warning("data keys = %r", data.keys())
#
#         for a in activities:
#             ad = cls._fixdate(a.start_datetime, tz).date()
#             ads = ad.isoformat()
#
#             logger.warning("%r - %r", ad, ad in data)
#             data[ads]["activities"].append(a)
#
#         logger.info("data %r", data)
#
#         return data
