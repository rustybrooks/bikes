from django.contrib.auth.models import User  # type: ignore
from django.core.management.base import BaseCommand, CommandError  # type: ignore

import bikes.models  # type: ignore


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        user = User.objects.filter(username="rbrooks").first()
        seasons = bikes.models.Season.objects.filter(user=user).order_by(
            "-season_start_date"
        )
        season = seasons[0]

        print(season)
        season.update_basic_weeks()
