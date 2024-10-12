import datetime
import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers  # type: ignore
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models, plans  # type: ignore
from bikes.models import Season, TrainingEntry, TrainingWeek
from bikes.plans import CTBv1

logger = logging.getLogger(__name__)


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        exclude: list[str] = []


class TrainingBibleV1In(serializers.Serializer):
    season_start_date = serializers.DateField()
    season_end_date = serializers.DateField()
    annual_hours = serializers.IntegerField()


class TrainingEntryOut(serializers.ModelSerializer):
    class Meta:
        model = TrainingEntry
        exclude: list[str] = []
        depth = 2

    workout_types = serializers.DictField()


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
        ctb = CTBv1({"annual_hours": request.data["annual_hours"]})
        progression = ctb.progression()

        weeks: list[TrainingWeek] = []
        start_date = (
            datetime.date.fromisoformat(request.data["season_start_date"])
            if request.data["season_start_date"]
            else None
        )
        end_date = (
            datetime.date.fromisoformat(request.data["season_end_date"])
            if request.data["season_end_date"]
            else None
        )
        logger.info("start=%r end=%r", start_date, end_date)

        season = Season(
            season_start_date=start_date,
            training_plan="CTB",
            params={"annual_hours": request.data["annual_hours"]},
        )

        entries = []
        this_day = start_date or datetime.date.today()
        prog_index = 0
        prog_ct = 1
        week_prog = progression[prog_index]
        while start_date:
            if prog_ct > week_prog[1]:
                prog_ct = 1
                prog_index += 1

            if prog_index >= len(progression):
                break

            if end_date and this_day > end_date:
                break

            week_prog = progression[prog_index]

            w = TrainingWeek(
                season=season,
                week_start_date=this_day,
                week_type=week_prog[0],
                week_type_num=prog_ct,
            )
            entries.extend(w.populate_entries(save=False))
            weeks.append(w)

            next_day = this_day + datetime.timedelta(days=7)

            this_day = next_day
            prog_ct += 1

        for to in entries:
            to.workout_types = {
                wt: ctb.workout_description(wt) for wt in to.workout_type_list()
            }

        training_serialized = TrainingEntryOut(data=entries, many=True)
        training_serialized.is_valid()
        training_entries_data = training_serialized.data

        data = {
            "entries": training_entries_data,
            "hour_selection": plans.training_bible_v1.annual_hours_lookup["Yearly"],
        }
        logger.info("data %r", data)
        serializer = TrainingBiblePreviewOut(data, many=False)
        logger.info("serialized %r", serializer.data)
        return Response(data)
