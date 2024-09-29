from rest_framework import serializers  # type: ignore
from rest_framework.viewsets import ModelViewSet  # type: ignore

from bikes import models  # type: ignore


class SeasonSerializer(serializers.Serializer):
    class Meta:
        model = models.Season
        exclude: list[str] = []

class SeasonViewSet(ModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = SeasonSerializer

