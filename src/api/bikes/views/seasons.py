import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers  # type: ignore
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet  # type: ignore

import bikes.models
from bikes import models  # type: ignore
from bikes.models import TrainingWeek
from bikes.plans import CTBv1


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = bikes.models.Season
        exclude: list[str] = []


class TrainingBibleV1In(serializers.Serializer):
    season_start_date = serializers.DateField()
    season_end_date = serializers.DateField()
    annual_hours = serializers.IntegerField()


class TrainingWeekOut(serializers.ModelSerializer):
    class Meta:
        model = bikes.models.TrainingWeek
        exclude: list[str] = []


class SeasonViewSet(ModelViewSet):
    queryset = bikes.models.Season.objects.all()
    serializer_class = SeasonSerializer
    ordering_fields = ["season_start_date", "season_end_date"]

    @swagger_auto_schema(
        request_body=TrainingBibleV1In, responses={200: TrainingWeekOut(many=True)}
    )
    @action(detail=False, methods=["post"])
    def preview_training_bible_v1(self, request: Request):
        ctb = CTBv1({"annual_hours": request.data["annual_hours"]})
        progression = ctb.progression()

        weeks = []
        this_day = request.data["season_start_date"]
        prog_index = 0
        prog_ct = 1
        week_prog = progression[prog_index]
        while this_day <= request.data["season_end_date"]:
            if prog_ct > week_prog[1]:
                prog_ct = 1
                if prog_index < len(progression) - 1:
                    prog_index += 1

            week_prog = progression[prog_index]

            w = TrainingWeek(
                season=self,
                week_start_date=this_day,
                week_type=week_prog[0],
                week_type_num=prog_ct,
            )
            w.populate_entries()
            weeks.append(w)

            next_day = this_day + datetime.timedelta(days=7)

            this_day = next_day
            prog_ct += 1

        return weeks
