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
    'strava_activity_segment_effort_achs', 'strava_activity_segment_efforts', 'strava_segments',
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
        activity_id bigint not null,
        external_id varchar(200),
        upload_id bigint,
        athelete_id bigint not null,
        activity_name varchar(200),
        distance real not null,
        moving_time int not null,
        total_elevation_gain real not null,
        elevation_high real,
        elevation_low real,
        type varchar(100) not null,
        start_datetime timestamp,
        start_datetime_local timestamp with time zone not null,
        timezone varchar(100) not null,
        start_lat real,
        start_long real,
        end_lat real,
        end_log real,
        achievement_count int not null,
        athlete_count int not null,
        -- map dunno,
        trainer bool not null default false,
        commute bool not null default false,
        manual bool not null default false,
        private bool not null default false,
        embed_token varchar(100),
        flagged bool not null default false,
        workout_type int,
        gear_id varchar(100),
        average_speed real,
        max_speed real,
        average_cadence real,
        average_temp real,
        average_watts real,
        max_watts real,
        weighted_average_watts real,
        kilojoules real,
        device_watts bool not null default false,
        average_heartrate real,
        max_heartrate real,
        suffer_score integer
    )
""")


initial.add_statement("""
    create table strava_segments(
        strava_segment_id serial primary key,
        resource_state int not null,
        name varchar(200) not null,
        activity_type varchar(100) not null,
        distance real not null,
        average_grade real not null,
        maxiumum_grade real not null,
        elevation_high real not null,
        elevation_low real not null,
        start_lat real,
        start_long real,
        end_lat real,
        end_long real,
        climb_category int,
        city varchar(200),
        state varchar(100),
        country varchar(200),
        private bool not null default false,
        starred bool not null default false,
        created_at timestamp,
        updated_at timestamp,
        total_elevation_game real,
        effort_count int not null,
        athlete_count int not null,
        hazardous bool not null default false,
        star_count int not null
    )
""")


initial.add_statement("""
    create table strava_activity_segment_efforts(
        strava_activity_segment_effort_id serial primary key,
        strava_activity_id bigint not null references strava_activities(strava_activity_id),
        resource_state int not null,
        name varchar(100) not null,
        elapsed_time int not null,
        moving_time int not null,
        start_datetime timestamp not null,
        end_datetime timestamp not null,
        start_index bigint not null,
        end_index bigint not null,
        average_cadence real,
        average_watts real,
        device_watts bool not null default false,
        average_heartrate real,
        max_heartrate real,
        strava_segment_id bigint references strava_segments(strava_segment_id) not null,
        kom_rank int,
        pr_rank int,
        hidden bool not null default false
    )
""")


initial.add_statement("""
    create table strava_activity_segment_effort_achs(
        strava_activity_segment_effort_ach_id bigserial primary key,
        strava_activity_segment_effort_id integer not null references strava_activity_segment_efforts(strava_activity_segment_effort_id),
        type_id integer not null,
        type varchar(100),
        rank integer not null
    )
""")



initial.add_statement("""
    create table strava_activity_streams(
        strava_activity_stream_id bigserial primary key,
        strava_activity_id bigint not null references strava_activities(strava_activity_id),
        time int not null,
        lat real,
        long real,
        distance real,
        altitude real,
        velocity_smooth real,
        heartrate real,
        cadence real,
        watts real,
        temp real,
        moving bool not null default false,
        grade_smooth real
    )
""")


initial.add_statement("""
    create table strava_segment_history_summaries(
        strava_segment_history_summary_id bigserial primary key,
        strava_segment_id integer not null references strava_segments(strava_segment_id),
        strava_activity integer not null references strava_activities(strava_activity_id) 
    )
""")


initial.add_statement("""
    create table strava_segment_histories(
        strava_segment_history_id bigserial primary key,
        strava_segment_id bigint not null references strava_segments(strava_segment_id),
        strava_activities bigint not null references strava_activities(strava_activity_id),
        recorded_datetime timestamp not null,
        rank int not null,
        entries int not null,
        average_heartrate real,
        average_watts real,
        distance real,
        elapsed_time int not null,
        moving_time int not null
    )
""")

initial.add_statement("""
    create table strava_power_curve(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        watts real not null,
        strava_activity_id integer not null references strava_activities(strava_activity_id)
    )
""")


initial.add_statement("""
    create table strava_speed_curve(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        speed real not null,
        strava_activity_id integer not null references strava_activities(strava_activity_id)
    )
""")


