# This is to manage the database structure

import logging
from warnings import filterwarnings

from lib.database.sql import Migration

logger = logging.getLogger(__name__)
filterwarnings('ignore', message='Invalid utf8mb4 character string')
filterwarnings('ignore', message='Duplicate entry')

##########################################################################################

initial = Migration(1, "initial version")
for table in [
    'strava_power_curves', 'strava_speed_curves',
    'strava_segment_histories', 'strava_segment_history_summaries',
    'strava_activity_segment_effort_achs', 'strava_activity_segment_efforts', 'strava_segments',
    'strava_activity_streams', 'strava_activities', 'users'
]:
    initial.add_statement("drop table if exists {}".format(table))


initial.add_statement("""
    create table users(
        user_id serial primary key,
        password varchar(200),
        email varchar(200),
        username varchar(50),
        access_token varchar(100),
        refresh_token varchar(100),
        expires_at timestamp
    )
""")
initial.add_statement("create index users_user_id on users(user_id)")

new = Migration(2, "strava stuff")
for table in [
    'strava_power_curves', 'strava_speed_curves',
    'strava_segment_histories', 'strava_segment_history_summaries',
    'strava_activity_segment_effort_achs', 'strava_activity_segment_efforts', 'strava_segments',
    'strava_activity_streams', 'strava_activities',
]:
    new.add_statement("drop table if exists {}".format(table))


new.add_statement("""
    create table strava_activities(
        strava_activity_id bigint primary key,
        user_id bigint not null references users(user_id),
        external_id varchar(500),
        athlete_id bigint,
        upload_id bigint,
        activity_name varchar(500),
        distance real not null,
        moving_time int not null,
        total_elevation_gain real not null,
        elevation_high real,
        elevation_low real,
        type varchar(100) not null,
        elapsed_time int not null,
        start_datetime timestamp,
        start_datetime_local timestamp not null,
        timezone varchar(100) not null,
        start_lat double precision,
        start_long double precision,
        end_lat double precision,
        end_long double precision,
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
        device_watts bool default false,
        average_heartrate real,
        max_heartrate real,
        suffer_score integer
    )
""")
new.add_statement("create index strava_activities_id on strava_activities(strava_activity_id)")
new.add_statement("create index strava_activities_user_id on strava_activities(user_id, strava_activity_id)")

new.add_statement("""
    create table strava_segments(
        strava_segment_id bigint primary key,
        resource_state int not null,
        name varchar(500) not null,
        activity_type varchar(100) not null,
        distance real not null,
        average_grade real not null,
        maximum_grade real not null,
        elevation_high double precision,
        elevation_low double precision,
        start_lat double precision,
        start_long double precision,
        end_lat double precision,
        end_long double precision,
        climb_category int,
        city varchar(200),
        state varchar(100),
        country varchar(200),
        private bool not null default false,
        starred bool not null default false,
        created_at timestamp,
        updated_at timestamp,
        total_elevation_gain real,
        effort_count int,
        athlete_count int,
        hazardous bool not null default false,
        star_count int
    )
""")
new.add_statement("create index strava_segments_id on strava_segments(strava_segment_id)")


new.add_statement("""
    create table strava_activity_segment_efforts(
        strava_activity_segment_effort_id serial primary key,
        strava_activity_id bigint not null references strava_activities(strava_activity_id),
        resource_state int not null,
        name varchar(500) not null,
        elapsed_time int not null,
        moving_time int not null,
        start_datetime timestamp not null,
        start_datetime_local timestamp with time zone not null,
        start_index bigint not null,
        end_index bigint not null,
        average_cadence real,
        average_watts real,
        device_watts bool default false,
        average_heartrate real,
        max_heartrate real,
        distance float,
        strava_segment_id bigint references strava_segments(strava_segment_id) not null,
        kom_rank int,
        pr_rank int,
        entries int,
        hidden bool not null default false
    )
""")
new.add_statement("create index strava_activity_segment_efforts_id on strava_activity_segment_efforts(strava_activity_segment_effort_id)")

new.add_statement("""
    create table strava_activity_segment_effort_achs(
        strava_activity_segment_effort_ach_id bigserial primary key,
        strava_activity_segment_effort_id integer not null references strava_activity_segment_efforts(strava_activity_segment_effort_id),
        type_id integer not null,
        type varchar(100),
        rank integer not null
    )
""")
new.add_statement("create index strava_activity_segment_effort_achs_id on strava_activity_segment_effort_achs(strava_activity_segment_effort_ach_id)")


new.add_statement("""
    create table strava_activity_streams(
        strava_activity_stream_id bigserial primary key,
        strava_activity_id bigint not null references strava_activities(strava_activity_id),
        time int not null,
        lat double precision,
        long double precision,
        distance real,
        altitude double precision,
        velocity_smooth real,
        heartrate real,
        cadence real,
        watts real,
        temp real,
        moving bool not null default false,
        grade_smooth real
    )
""")
new.add_statement("create index strava_activity_streams_id on strava_activity_streams(strava_activity_stream_id)")
new.add_statement("create index strava_activity_streams_activity_id on strava_activity_streams(strava_activity_id)")


new.add_statement("""
    create table strava_power_curves(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        watts real not null,
        strava_activity_id bigint not null references strava_activities(strava_activity_id)
    )
""")
new.add_statement("create index strava_power_curves_id on strava_power_curves(strava_power_curve_id)")
new.add_statement("create index strava_power_curves_activity_id on strava_power_curves(strava_activity_id)")

new.add_statement("""
    create table strava_speed_curves(
        strava_power_curve_id bigserial primary key,
        interval_length int not null,
        speed real not null,
        strava_activity_id bigint not null references strava_activities(strava_activity_id)
    )
""")
new.add_statement("create index strava_speed_curves_id on strava_speed_curves(strava_power_curve_id)")
new.add_statement("create index strava_speed_curves_activity_id on strava_speed_curves(strava_activity_id)")


