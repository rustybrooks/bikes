import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status  # type: ignore
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models, plans  # type: ignore
from bikes.models import Season
from bikes.views.training_entry import TrainingEntryOut

logger = logging.getLogger(__name__)


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        exclude: list[str] = []


class TrainingBibleV1In(serializers.Serializer):
    season_start_date = serializers.DateField(allow_null=True)
    season_end_date = serializers.DateField(allow_null=True)
    params = serializers.JSONField()


class TrainingBiblePreviewOut(serializers.Serializer):
    entries = serializers.ListField(child=TrainingEntryOut())
    hour_selection = serializers.ListField(child=serializers.IntegerField())


class SeasonViewSet(ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    ordering_fields = ["season_start_date", "season_end_date"]

    @swagger_auto_schema(
        request_body=TrainingBibleV1In,
        responses={200: openapi.Response("", TrainingBiblePreviewOut(many=False))},
    )
    @action(detail=False, methods=["post"])
    def preview_training_bible_v1(self, request: Request):
        serializer = TrainingBibleV1In(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        season, weeks, entries = Season.generate_weeks(
            user=None, **serializer.validated_data
        )

        training_serialized = TrainingEntryOut(data=entries, many=True)
        training_serialized.is_valid()
        training_entries_data = training_serialized.data

        data = {
            "entries": training_entries_data,
            "hour_selection": plans.training_bible_v1.annual_hours_lookup["Yearly"],
        }
        return Response(data)
