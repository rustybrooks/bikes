#!/usr/bin/env python3

#  This is intended to be run periodically to sync data
# matches on hand

import optparse
import logging
import multiprocessing
import os
import sys
import time
import traceback

logging.basicConfig(level=logging.WARN, format="[%(levelname)s %(asctime)s %(module)s.%(funcName)s] %(message)s")
logger = logging.getLogger(__name__)

os.environ['FLASK_STORAGE'] = '0'

basedir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(basedir, '..')))

from lib.database.sql import Migration
from bikedb import queries, migrations


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
        # if options.sync:
        #     if options.from_cache:
        #         sync_players.sync_from_disk(load_assets=options.load_assets, pubg_match_id=options.pubg_match_id)
        #     else:
        #         try:
        #             sync_players.sync(load_assets=options.load_assets, pubg_match_id=options.pubg_match_id)
        #         except Exception:
        #             logger.error("Exception while syncing: %r", traceback.format_exc())

        if options.continuous < 0:
            break

        left = max(0, options.continuous - (time.time()-t1))
        time.sleep(left)

        logger.warning("Done sync")
