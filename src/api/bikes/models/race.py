from django.db import models  # type: ignore

from bikes.models import Season  # type: ignore


class Race(models.Model):
    PRIORITY_CHOICES = (("A", "A"), ("B", "B"), ("C", "C"))

    season = models.ForeignKey(Season, on_delete=models.DO_NOTHING)
    race_date = models.DateField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)

    def __unicode__(self):
        return "%s -- %s" % (self.name, self.race_date)
