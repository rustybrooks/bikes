#
#     @classmethod
#     @Api.config(require_login=is_logged_in)
#     def heatmap(cls):
#         fn = heatmap.generate(
#             type="Ride",
#             start_date=datetime.datetime(2018, 1, 1),
#         )
#         resp = HttpResponse(
#             content=open(fn, "rb").read(),
#             content_type="image/png",
#         )
#         os.unlink(fn)
#         return resp

