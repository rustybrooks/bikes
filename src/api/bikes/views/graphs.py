import datetime
import logging
from collections import defaultdict

from django.db.models.aggregates import Count, Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, viewsets  # type: ignore
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models, plans  # type: ignore
from bikes.models import StravaActivity

logger = logging.getLogger(__name__)


class ProgressGraphDataPointOut(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    time = serializers.FloatField()
    distance = serializers.FloatField()


class ProgressGraphIn(serializers.Serializer):
    start_date = serializers.DateField(allow_null=True, required=False)
    end_date = serializers.DateField(allow_null=True, required=False)
    workout_type = serializers.CharField(allow_null=True, required=False)


class ProgressGraphOut(serializers.Serializer):
    year = serializers.IntegerField()
    data = serializers.ListField(child=ProgressGraphDataPointOut())


class GraphsViewSet(viewsets.GenericViewSet):
    @swagger_auto_schema(
        request_body=ProgressGraphIn,
        responses={200: openapi.Response("", ProgressGraphOut(many=True))},
    )
    @action(detail=False, methods=["post"])
    def progress(self, request: Request):
        serializer = ProgressGraphIn(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        vdata = serializer.validated_data
        query_data = {}
        if start_date := vdata.get("start_date"):
            query_data["start_datetime__gte"] = start_date

        if end_date := vdata.get("end_date"):
            query_data["start_datetime__lt"] = end_date

        if workout_type := vdata.get("workout_type"):
            query_data["type"] = workout_type

        workouts: list[StravaActivity] = (
            StravaActivity.objects.filter(**query_data)
            .values("start_datetime")
            .order_by("start_datetime_local")
            .annotate(distance_sum=Sum("distance"))
            .annotate(time_sum=Sum("moving_time"))
        )

        cum_time = defaultdict(float)
        cum_dist = defaultdict(float)

        series_data = []
        this_series = []
        last_year = None
        for w in workouts:
            if last_year is not None and last_year != w["start_datetime"].year:
                series_data.append({"year": last_year, "data": this_series})
                this_series = []

            last_year = w["start_datetime"].year

            data_key = w["start_datetime"].year
            cum_time[data_key] += w["time_sum"]
            cum_dist[data_key] += w["distance_sum"]

            this_series.append(
                {
                    "timestamp": w["start_datetime"],
                    "time": cum_time[data_key],
                    "distance": cum_dist[data_key],
                }
            )

        if this_series:
            series_data.append({"year": last_year, "data": this_series})

        out_ser = ProgressGraphOut(data=series_data, many=True)
        out_ser.is_valid()

        return Response(out_ser.data)
