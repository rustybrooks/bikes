import logging
import os
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
    sql_url = "postgresql://wombat:1wombat2@local-bikedb-postgres.aveng.us:5432/bikes"
else:
    sql_url = 'postgresql://bikedb:{}@flannelcat-postgres.cwrbtizazqua.us-west-2.rds.amazonaws.com:5432/bikes'.format(
        config.get_config_key('DB_PASSWORD')
    )

SQL = SQLFactory(sql_url, flask_storage=os.environ.get('FLASK_STORAGE', "1'") != "0")