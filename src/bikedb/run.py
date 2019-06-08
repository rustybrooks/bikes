#!/usr/bin/env python3

#  This is intended to be run periodically to sync data
# matches on hand

import optparse
import logging
import os
import sys
import time

os.environ['FLASK_STORAGE'] = '0'

basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(basedir, '..')))

from lib.database.sql import Migration
from bikedb import queries, stravaapi

logging.basicConfig(level=logging.WARN, format="[%(levelname)s %(asctime)s %(module)s.%(funcName)s] %(message)s")
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-c', '--continuous', type=int, default=-1, help='Sync continuously with given interval in seconds')
    parser.add_option('-m', '--migrate', action='store_true', default=False, help='Perform migration on startup')
    parser.add_option('-s', '--sync', action='store_true', default=False, help='Perform sync on startup')
    parser.add_option('-i', '--initial', action='store_true', default=False, help="Whether to do a full migration from initial state")
    parser.add_option('-a', '--apply', type=str, default=None, help="Migration version to manually apply")
    options, args = parser.parse_args()

    if options.migrate:
        apply = [int(x) for x in options.apply.split(',')] if options.apply else []
        Migration.migrate(SQL=queries.SQL, dry_run=False, initial=options.initial, apply_versions=apply)

    while True:
        t1 = time.time()
        logger.warning("Starting sync")

        for u in [queries.User(user_id=x.user_id) for x in queries.users()]:
            logger.warning("Syncing user %r", u)
            stravaapi.activities_sync_many(u, days_ago=1)

        logger.warning("Done sync")

        if options.continuous < 0:
            break

        left = max(0, options.continuous - (time.time()-t1))
        time.sleep(left)

