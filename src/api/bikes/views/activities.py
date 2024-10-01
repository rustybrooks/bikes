from django.contrib.auth.models import User  # type: ignore  # type: ignore
from rest_framework import mixins, serializers, status, viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet  # type: ignore

import bikes.models.strava_activity
from bikes import models  # type: ignore


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude: list[str] = []


class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = bikes.models.strava_activity.StravaActivity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
