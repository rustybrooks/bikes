import datetime

from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bikes.models import Season, TrainingEntry, TrainingWeek
from bikes.views.activity import range_filters
from bikes.views.training_entry import TrainingEntryOut


class TrainingWeekOut(serializers.ModelSerializer):
    class Meta:
        model = TrainingWeek
        exclude: list[str] = []
        depth = 0


class TrainingWeekPopulateIn(serializers.Serializer):
    season_start_date = serializers.DateField(allow_null=True)
    season_end_date = serializers.DateField(allow_null=True)
    training_plan = serializers.CharField()
    params = serializers.JSONField()


class TrainingWeekViewSet(ModelViewSet):
    queryset = TrainingWeek.objects.all()
    serializer_class = TrainingWeekOut
    permission_classes = [IsAuthenticated]

    filterset_fields = {"week_start_date": range_filters}
    search = []
    ordering_fields = []

    @swagger_auto_schema(
        request_body=TrainingWeekPopulateIn, responses={200: TrainingWeekOut}
    )
    @action(detail=False, methods=["post"])
    @transaction.atomic
    def populate(self, request: Request):
        serializer = TrainingWeekPopulateIn(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        season, weeks, entries = Season.generate_weeks(
            user=request.user,
            season_start_date=serializer.validated_data["season_start_date"],
            season_end_date=serializer.validated_data["season_end_date"],
            params=serializer.validated_data["params"],
        )
        season.save()
        TrainingWeek.objects.bulk_create(weeks)
        TrainingEntry.objects.bulk_create(entries)

        out_ser = TrainingEntryOut(data=entries, many=True)
        out_ser.is_valid()

        return Response(out_ser.data)
