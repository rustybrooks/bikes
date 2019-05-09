# This is to manage the database structure

import logging
from warnings import filterwarnings
import psycopg2

from lib.database.sql import Migration

logger = logging.getLogger(__name__)
filterwarnings('ignore', message='Invalid utf8mb4 character string')
filterwarnings('ignore', message='Duplicate entry')

##########################################################################################

initial = Migration(1, "initial version")
for table in [
    'strava_power_curves', 'strava_speed_curves', 'strava_segment_histories', 'strava_segment_history_summaries',
    'strava_activity_segment_effor_achs', 'strava_activity_segment_efforts', 'strava_segments'
    'strava_activities', 'users'
]:
    initial.add_statement("drop table if exists {}".format(table))


initial.add_statement("""
    create table users(
        user_id serial primary key
    )
""")

initial.add_statement("""
    create table strava_activities(
        strava_activity_id serial primary key,
        user_id bigint not null references users(user_id),
        activity_id bigint,
        external_id smalltext,
        upload_id bigint,
        athelete_id bigint,
        activity_name smalltext,
        distance float,
        moving_time int,
        total_elevation_gain float,
        elev_high float,
        elev_low float,
        type varchar(100),
        start_datetime timestamp,
        start_datetime_local timestamp with timezone,
        timezone = varchar(100),
        start_lat float,
        start_long float,
        end_lat float,
        end_log float,
        achievement_count int,
        athlete_count int,
        -- map dunno,
        trainer bool,
        commute bool,
        manual bool,
        private bool,
        embed_token varchar(100),
        flagged bool,
        workout_type int,
        gear_id = varchar(100),
        average_speed float,
        max_speed float,
        average_cadence float,
        average_temp float,
        average_watts float,
        max_watts float,
        weighted_average_watts float,
        kilojoules watts,
        device_watts bool,
        average_heartrate float,
        max_heartrate float,
        suffer_score integer
    )
""")


initial.add_statement("""
    create_table strava_segments(
        strava_segment_id serial primary key,
        resource_state int,
        name varchar(200),
        activity_type varchar(100),
        distance float,
        average_grade float,
        maxiumum_grade float,
        elevation_high float,
        elevation_low float,
        start_lat float,
        start_long float,
        end_lat float,
        end_long float,
        climb_category int,
        city varchar(200),
        state varchar(100),
        country charchar(200),
        private bool,
        starred bool,
        created_at timestamp,
        updated_at timestamp,
        total_elevation_game float,
        effort_count int,
        athlete_count int,
        hazardous bool,
        star_count int
    )
""")


initial.add_statement("""
    create_table strava_activity_segment_efforts(
        strava_activity_segment_effort_id serial primary key,
        strava_activity_id references strava_activities(strava_activity_id),
        resource_state int,
        name varchar(100),
        elapsed_time int,
        moving_time int,
        start_datetime timestamp,
        end_datetime timestamp,
        start_index bigint,
        end_index bigint,
        average_cadence float,
        average_watts float,
        device_watts bool,
        average_heartrate float,
        max_heartrate float,
        segment references strava_segments(strava_segment_id)
        kom_rank int,
        pr_rank int,
        hidden bool
    )
""")


initial.add_statement("""
    create_table strava_activity_segment_effort_achs(
        strava_activity_segment_effort_ach_id bigserial primary key
        strava_activity_segment_effort_id integer not null references strava_activity_segments(strava_activity_segment_effort_id)
        type_id integer not null,
        type varchar(100),
        rank integer not null
    )
""")



initial.add_statement("""
    create_table strava_activity_streams(
        strava_activity_stream_id bigserial primary key,
        strava_activity_id bigint not null strava_activities(strava_activity_id),
        time timestamp not null,
        lat float not null,
        long float not null,
        distance float not null,
        altitude float not null,
        velocity_smooth float not null,
        heartrate float not null,
        cadence float not null,
        watts float not null,
        temp float not null,
        moving bool not null,
        grade_smooth float not null
    )
""")


initial.add_statement("""
    create_table strava_segment_history_summaries(
        strava_segment_history_summary_id bigserial primary key,
        strava_segment_id integer not null references strava_segments(strava_segment_id),
        strava_activity integer not null references strava_activities(strava_activity_id) 
    )
""")


initial.add_statement("""
    create_table strava_segment_histories(
        strava_segment_history_id bigserial primary key,
        strava_segment_id bigint not null references strava_segments(strava_segment_id)
        strava_activities bigint not null references strava_activities(strava_activity_id)
        recorded_datetime timestamp not null,
        rank int not null,
        entries int not null,
        average_heartrate float,
        average_watts float,
        distance float,
        elapsed_time int not null,
        moving_time int not null
    )
""")

initial.add_statement("""
    create_table strava_power_curve(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        watts float not null,
        strava_activity_id integer not null references strava_activities(strava_activity_id)
    )
""")


initial.add_statement("""
    create_table strava_speed_curve(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        speed float not null,
        strava_activity_id integer not null references strava_activities(strava_activity_id)
    )
""")


