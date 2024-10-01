from rest_framework import serializers  # type: ignore
from rest_framework.viewsets import ModelViewSet  # type: ignore

import bikes.models.season
from bikes import models  # type: ignore


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = bikes.models.activity.Season
        exclude: list[str] = []


class SeasonViewSet(ModelViewSet):
    queryset = bikes.models.activity.Season.objects.all()
    serializer_class = SeasonSerializer
