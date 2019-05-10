import bcrypt
import hashlib
import logging
import os
import random

from lib.database.sql import SQLBase, dictobj, chunked
from lib import config

# filterwarnings('ignore', category = pymysql.Warning)

basedir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


_SQL = None
isolation_level = 'REPEATABLE READ'


def SQLFactory(sql_url=None, flask_storage=False):
    global _SQL
    if _SQL is None:
        logger.warning("Initializing SQL: %r, flask_storage=%r", sql_url, flask_storage)
        _SQL = SQLBase(
            sql_url,
            isolation_level=isolation_level,
            echo_pool=True,
            pool_recycle=60*60*2,
            flask_storage=flask_storage,

        )
        logger.warning("Done Initializing SQL: %r, flask_storage=%r", sql_url, flask_storage)

    return _SQL


if config.get_config_key('ENVIRONMENT') == 'dev':
    sql_url = "postgresql://wombat:1wombat2@local-bikes-postgres.aveng.us:5432/bikes"
else:
    sql_url = 'postgresql://bikedb:{}@flannelcat-postgres.cwrbtizazqua.us-west-2.rds.amazonaws.com:5432/bikes'.format(
        config.get_config_key('DB_PASSWORD')
    )

SQL = SQLFactory(sql_url, flask_storage=os.environ.get('FLASK_STORAGE', "1'") != "0")


class User(object):
    def __unicode__(self):
        return u"User(username={}, user_id={})".format(getattr(self, 'username'), getattr(self, 'user_id'))

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def to_json(self):
        return {
            'user_id': self.user_id,
        }

    def __init__(self, user_id=None, username=None, email=None, password=None, is_authenticated=False):
        self.is_authenticated = is_authenticated
        self.is_active = False
        self.is_anonymous = False
        self.user_id = 0

        where, bindvars = SQL.auto_where(username=username, user_id=user_id, email=email)

        query = "select * from users {}".format(SQL.where_clause(where))
        r = SQL.select_0or1(query, bindvars)

        if r:
            for k, v in r.items():
                setattr(self, k, v)

            if password is not None:
                self.authenticate(password)

    def authenticate(self, password):
        salt = self.password[:29].encode('utf-8')
        genpass = self.generate_password_hash(password, salt)
        ourpass = bytes(self.password.encode('utf-8'))
        logger.warning("%r salt=%r, ourpass=%r, genpass=%r", password, salt, ourpass, genpass)
        self.is_authenticated = ourpass and (genpass == ourpass)
        self.is_active = self.is_authenticated
        return self.is_authenticated

    @classmethod
    def generate_password_hash(cls, password, salt):
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def get_id(self):
        return str(self.user_id)


def add_user(username=None, email=None, password=None):
    salt = bcrypt.gensalt(12)
    return SQL.insert('users', {
        'username': username,
        'email': email,
        'password': User.generate_password_hash(password, salt).decode('utf-8'),
    })


def update_user(user_id=None, refresh_token=None, access_token=None, expires_at=None):
    data = {
        'refresh_token': refresh_token,
        'access_token': access_token,
        'expires_at': expires_at
    }
    SQL.update('users', 'user_id=:user_id', where_data={'user_id': user_id}, data=data)


def delete_user(username=None, email=None):
    where, bindvars = SQL.auto_where(username=username, email=email)
    SQL.delete('users', where, bindvars)