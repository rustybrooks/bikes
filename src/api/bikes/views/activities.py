import logging

from django.contrib.auth.models import User  # type: ignore  # type: ignore
from rest_framework import mixins, serializers, status, viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models  # type: ignore
from bikes.models import StravaActivity  # type: ignore

logger = logging.getLogger(__name__)


class ActivityOut(serializers.ModelSerializer):
    class Meta:
        model = StravaActivity
        exclude: list[str] = []


range_filters = ["exact", "gt", "lt", "gte", "lte"]


class ActivitiesViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = StravaActivity.objects.all()
    serializer_class = ActivityOut
    permission_classes = [IsAuthenticated]

    filterset_fields = {
        "type": ["exact"],
        "trainer": ["exact"],
        "commute": ["exact"],
        "manual": ["exact"],
        "private": ["exact"],
        "flagged": ["exact"],
        "start_datetime": range_filters,
        "start_datetime_local": range_filters,
        "moving_time": range_filters,
        "elapsed_time": range_filters,
        "total_elevation_gain": range_filters,
        "achievement_count": range_filters,
        "average_speed": range_filters,
        "max_speed": range_filters,
        "average_watts": range_filters,
        "max_watts": range_filters,
        "weighted_average_watts": range_filters,
        "kilojoules": range_filters,
        "average_heartrate": range_filters,
        "max_heartrate": range_filters,
        "suffer_score": range_filters,
    }
    search = ["activity_name", "type"]

    ordering_fields = [
        "start_datetime",
        "start_datetime_local",
        "moving_time",
        "elapsed_time",
        "total_elevation_gain",
        "type",
        "achievement_count",
        "average_speed",
        "max_speed",
        "average_watts",
        "max_watts",
        "weighted_average_watts",
        "kilojoules",
        "average_heartrate",
        "max_heartrate",
        "suffer_score",
    ]
