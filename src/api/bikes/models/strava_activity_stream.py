from django.db import models  # type: ignore


class StravaActivityStream(models.Model):
    activity_stream_id = models.AutoField(primary_key=True)
    activity = models.ForeignKey("StravaActivity", on_delete=models.DO_NOTHING)
    time = models.IntegerField()
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    distance = models.FloatField(null=True)
    altitude = models.FloatField(null=True)
    velocity_smooth = models.FloatField(null=True)
    heartrate = models.IntegerField(null=True)
    cadence = models.IntegerField(null=True)
    watts = models.IntegerField(null=True)
    temp = models.IntegerField(null=True)
    moving = models.BooleanField(default=False, null=True)
    grade_smooth = models.FloatField(null=True)

    def json(self):
        fields = [
            "time",
            "lat",
            "long",
            "distance_mi",
            "altitude",
            "speed_mph",
            "heartrate",
            "cadence",
            "watts",
            "temp",
            "moving",
            "grade_smooth",
        ]
        return {f: getattr(self, f) for f in fields}

    @property
    def distance_mi(self):
        return (self.distance or 0) / 1609.34

    @property
    def speed_mph(self):
        return ((self.velocity_smooth or 0) / 1609.34) * 3600

    # Note, this actually downloads the data too, via the API
    @classmethod
    def sync(cls, user, activity, force=False):
        from bikes.libs import stravaapi
        from bikes.models import StravaPowerCurve, StravaSpeedCurve

        current = cls.objects.filter(activity=activity)
        if len(current) and not force:
            return

        cls.objects.filter(activity=activity).delete()

        stream_data = stravaapi.get_activity_stream(user, activity.activity_id)
        types = []
        datas = []
        for stream in stream_data:
            types.append(stream["type"])
            datas.append(stream["data"])

        objs = []
        for datum in zip(*datas):
            # logger.warning("%r", zip(types, datum))
            s = StravaActivityStream()
            s.activity = activity
            for t, d in zip(types, datum):
                if t == "latlng":
                    s.lat = d[0]
                    s.long = d[1]
                else:
                    setattr(s, t, d)

            objs.append(s)

        StravaActivityStream.objects.bulk_create(objs)

        StravaPowerCurve.process_curve(activity.activity_id)
        StravaSpeedCurve.process_curve(activity.activity_id)
