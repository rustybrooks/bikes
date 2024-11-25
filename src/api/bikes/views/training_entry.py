from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from bikes.models import TrainingEntry
from bikes.plans import CTBv1
from bikes.views.activity import range_filters


class TrainingEntryOut(serializers.ModelSerializer):
    class Meta:
        model = TrainingEntry
        exclude: list[str] = []
        depth = 0

    workout_types = serializers.SerializerMethodField(allow_null=False)

    @classmethod
    def get_workout_types(cls, obj) -> dict:
        return {wt: CTBv1.workout_description(wt) for wt in obj.workout_type_list()}


class TrainingEntryViewSet(ModelViewSet):
    queryset = TrainingEntry.objects.all().select_related("week", "season")
    serializer_class = TrainingEntryOut
    permission_classes = [IsAuthenticated]

    filterset_fields = {
        "week__id": ["exact"],
        "workout_type": ["exact"],
        "activity_type": ["exact"],
        "scheduled_dow": ["exact"],
        "scheduled_length": ["exact"],
        "actual_length": ["exact"],
        "week__week_start_date": range_filters,
    }
    search = []
    ordering_fields = [
        "week",
        "workout_type",
        "activity_type",
    ]
