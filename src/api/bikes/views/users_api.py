# from typing import Optional
#
# import flask_login  # type: ignore
# from api_framework import Api, api_register  # type: ignore
#
# from bikedb import queries  # type: ignore
#
#
# @api_register(None, require_login=False)
# class Users(Api):
#     @classmethod
#     def login(cls, username=None, password=None):
#         user = queries.User(username=username, password=password)
#         if user.is_authenticated():
#             flask_login.login_user(user)
#         else:
#             raise Api.Forbidden("Invalid username or password")
