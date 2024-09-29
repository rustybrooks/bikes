# import logging
#
# import flask_login  # type: ignore
# # from api_framework import FlaskUser
#
# logger = logging.getLogger(__name__)
#
# def is_logged_in(request, api_data, url_data):
#     logger.warning("is_logged_in %r - %r", flask_login.current_user.__class__, flask_login.current_user)
#
#     if isinstance(flask_login.current_user, flask_login.mixins.AnonymousUserMixin):
#         flask_login.current_user.is_authenticated = lambda *args, **kwargs: False
#
#     return flask_login.current_user
