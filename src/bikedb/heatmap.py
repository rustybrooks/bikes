import datetime
import os
import sys
import tempfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from lib import heatmaplib
from bikedb import queries


def generate(start_date=None, end_date=None, type=None, type_in=None):
    coords = queries.activity_streams(
        start_datetime_before=end_date, start_datetime_after=start_date, type=type, type_in=type_in
    )

    with tempfile.NamedTemporaryFile(mode="w+b", suffix='.png', delete=False) as tf:
        name = tf.name
        heatmaplib.make_heatmap(
            output=tf.name, data=[(x.lat, x.long) for x in coords],
            height=1000, background='black'

        )

    return name
