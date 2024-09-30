# Generated by Django 5.0.9 on 2024-09-30 20:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StravaSegment',
            fields=[
                ('segment_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('resource_state', models.IntegerField()),
                ('name', models.TextField()),
                ('activity_type', models.TextField()),
                ('distance', models.FloatField()),
                ('average_grade', models.FloatField()),
                ('maximum_grade', models.FloatField()),
                ('elevation_high', models.FloatField()),
                ('elevation_low', models.FloatField()),
                ('start_lat', models.FloatField(null=True)),
                ('start_long', models.FloatField(null=True)),
                ('end_lat', models.FloatField(null=True)),
                ('end_long', models.FloatField(null=True)),
                ('climb_category', models.IntegerField()),
                ('city', models.TextField(null=True)),
                ('state', models.TextField(null=True)),
                ('country', models.TextField(null=True)),
                ('private', models.BooleanField(default=False)),
                ('starred', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('total_elevation_gain', models.FloatField(null=True)),
                ('effort_count', models.IntegerField(null=True)),
                ('athlete_count', models.IntegerField(null=True)),
                ('hazardous', models.BooleanField(default=False)),
                ('star_count', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_plan', models.CharField(choices=[('CTB', "Cyclist's Training Bible"), ('TCC', 'Time Crunched Cyclist')], max_length=100)),
                ('season_start_date', models.DateField()),
                ('season_end_date', models.DateField()),
                ('params', models.CharField(max_length=5000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_date', models.DateField()),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('priority', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.season')),
            ],
        ),
        migrations.CreateModel(
            name='StravaActivity',
            fields=[
                ('activity_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('external_id', models.TextField(null=True)),
                ('upload_id', models.BigIntegerField(null=True)),
                ('athlete_id', models.BigIntegerField()),
                ('activity_name', models.TextField(null=True)),
                ('distance', models.FloatField()),
                ('moving_time', models.IntegerField()),
                ('elapsed_time', models.IntegerField()),
                ('total_elevation_gain', models.FloatField()),
                ('elev_high', models.FloatField(null=True)),
                ('elev_low', models.FloatField(null=True)),
                ('type', models.TextField()),
                ('start_datetime', models.DateTimeField(null=True)),
                ('start_datetime_local', models.DateTimeField()),
                ('timezone', models.TextField()),
                ('start_lat', models.FloatField(null=True)),
                ('start_long', models.FloatField(null=True)),
                ('end_lat', models.FloatField(null=True)),
                ('end_long', models.FloatField(null=True)),
                ('achievement_count', models.IntegerField()),
                ('athlete_count', models.IntegerField()),
                ('trainer', models.BooleanField(default=False)),
                ('commute', models.BooleanField(default=False)),
                ('manual', models.BooleanField(default=False)),
                ('private', models.BooleanField(default=False)),
                ('embed_token', models.TextField(null=True)),
                ('flagged', models.BooleanField(default=False)),
                ('workout_type', models.IntegerField(null=True)),
                ('gear_id', models.TextField(null=True)),
                ('average_speed', models.FloatField(null=True)),
                ('max_speed', models.FloatField(null=True)),
                ('average_cadence', models.FloatField(null=True)),
                ('average_temp', models.FloatField(null=True)),
                ('average_watts', models.FloatField(null=True)),
                ('max_watts', models.FloatField(null=True)),
                ('weighted_average_watts', models.FloatField(null=True)),
                ('kilojoules', models.FloatField(null=True)),
                ('device_watts', models.BooleanField(default=False, null=True)),
                ('average_heartrate', models.FloatField(null=True)),
                ('max_heartrate', models.FloatField(null=True)),
                ('suffer_score', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StravaActivitySegmentEffort',
            fields=[
                ('activity_segment_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('resource_state', models.IntegerField()),
                ('name', models.TextField()),
                ('elapsed_time', models.IntegerField()),
                ('moving_time', models.IntegerField()),
                ('start_datetime', models.DateTimeField()),
                ('start_datetime_local', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('start_index', models.BigIntegerField()),
                ('end_index', models.BigIntegerField()),
                ('average_cadence', models.FloatField(null=True)),
                ('average_watts', models.FloatField(null=True)),
                ('device_watts', models.BooleanField(default=False, null=True)),
                ('average_heartrate', models.FloatField(null=True)),
                ('max_heartrate', models.FloatField(null=True)),
                ('kom_rank', models.IntegerField(null=True)),
                ('pr_rank', models.IntegerField(null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravasegment')),
            ],
        ),
        migrations.CreateModel(
            name='StravaActivitySegmentEffortAch',
            fields=[
                ('achievement_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_id', models.IntegerField()),
                ('type', models.TextField()),
                ('rank', models.IntegerField()),
                ('segment_effort', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivitysegmenteffort')),
            ],
        ),
        migrations.CreateModel(
            name='StravaActivityStream',
            fields=[
                ('activity_stream_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.IntegerField()),
                ('lat', models.FloatField(null=True)),
                ('long', models.FloatField(null=True)),
                ('distance', models.FloatField(null=True)),
                ('altitude', models.FloatField(null=True)),
                ('velocity_smooth', models.FloatField(null=True)),
                ('heartrate', models.IntegerField(null=True)),
                ('cadence', models.IntegerField(null=True)),
                ('watts', models.IntegerField(null=True)),
                ('temp', models.IntegerField(null=True)),
                ('moving', models.BooleanField(default=False, null=True)),
                ('grade_smooth', models.FloatField(null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
            ],
        ),
        migrations.CreateModel(
            name='StravaPowerCurve',
            fields=[
                ('power_curve_id', models.AutoField(primary_key=True, serialize=False)),
                ('interval_length', models.IntegerField()),
                ('watts', models.FloatField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
            ],
        ),
        migrations.CreateModel(
            name='StravaSegmentHistory',
            fields=[
                ('segment_history_id', models.AutoField(primary_key=True, serialize=False)),
                ('recorded_datetime', models.DateTimeField()),
                ('rank', models.IntegerField()),
                ('entries', models.IntegerField()),
                ('average_hr', models.FloatField(null=True)),
                ('average_watts', models.FloatField(null=True)),
                ('distance', models.FloatField(null=True)),
                ('elapsed_time', models.IntegerField()),
                ('moving_time', models.IntegerField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravasegment')),
            ],
        ),
        migrations.CreateModel(
            name='StravaSegmentHistorySummary',
            fields=[
                ('segment_history_summary_id', models.AutoField(primary_key=True, serialize=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
                ('segment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravasegment')),
            ],
        ),
        migrations.CreateModel(
            name='StravaSpeedCurve',
            fields=[
                ('speed_curve_id', models.AutoField(primary_key=True, serialize=False)),
                ('interval_length', models.IntegerField()),
                ('speed', models.FloatField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.stravaactivity')),
            ],
        ),
        migrations.CreateModel(
            name='StravaTokens',
            fields=[
                ('strava_token_id', models.AutoField(primary_key=True, serialize=False)),
                ('access_token', models.TextField(null=True)),
                ('refresh_token', models.TextField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start_date', models.DateField()),
                ('week_type', models.CharField(max_length=50)),
                ('week_type_num', models.IntegerField()),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.season', unique_for_date='week_start_date')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateField()),
                ('workout_type', models.CharField(max_length=50)),
                ('scheduled_dow', models.IntegerField()),
                ('scheduled_length', models.FloatField()),
                ('scheduled_length2', models.FloatField()),
                ('actual_length', models.FloatField()),
                ('notes', models.CharField(max_length=2000)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.season', unique_for_date='entry_date')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bikes.week')),
            ],
        ),
    ]
