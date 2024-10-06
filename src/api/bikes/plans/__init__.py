from . import tcc as tccdata  # type: ignore
from . import training_bible_v1 as tbv1data  # type: ignore


class TrainingPlan:
    def __init__(self, params):
        self.params = params


class TCC(TrainingPlan):
    def progression(self):
        return tccdata.progression

    def plan_entries(self, week):
        key = "%s" % (week.week_type,)
        patterns = tccdata.workout_patterns[self.params["type"]][key]

        # key = "%s" % (week.week_type,)
        # hpatterns = tccdata.hour_patterns[key]

        # week_hours = tccdata.weekly_hours_lookup[week.weekly_hours()]
        start_index = (int(week.week_start_date.strftime("%w")) - 1) % 7

        entries = []
        for dow in range(0, 7):
            dow_ind = (dow + start_index) % 7
            wotype = patterns[dow_ind][0]

            # if dow not in entry_by_orig:
            entries.append(
                dict(
                    dow=dow,
                    workout_type=wotype,
                    scheduled_dow=dow_ind,
                    scheduled_length=tccdata.workout_details[self.params["type"]][
                        week.week_type
                    ][dow_ind][0],
                    scheduled_length2=tccdata.workout_details[self.params["type"]][
                        week.week_type
                    ][dow_ind][1],
                    actual_length=tccdata.workout_details[self.params["type"]][
                        week.week_type
                    ][dow_ind][1],
                )
            )

        return entries

    def weekly_hours(self, week):
        # pass
        return 7

    def workout_description(self, wo_type):
        return "temp"

    def workout_types(self, entry):
        key = "%s" % (entry.week.week_type,)
        patterns = tccdata.workout_patterns[key]
        return patterns[entry.scheduled_dow]


class CTBv1(TrainingPlan):
    def progression(self):
        return tbv1data.progresssion

    def weekly_hours(self, week):
        yearlies = tbv1data.annual_hours_lookup["Yearly"]
        i = yearlies.index(self.params["annual_hours"])

        try:
            key = "%s-%s" % (week.week_type, week.week_type_num)
            hours = tbv1data.annual_hours_lookup[key][i]
        except KeyError:
            key = "%s" % (week.week_type,)
            hours = tbv1data.annual_hours_lookup[key][i]

        return hours

    def plan_entries(self, week):
        try:
            key = "%s-%s" % (week.week_type, week.week_type_num)
            patterns = tbv1data.workout_patterns[key]
        except KeyError:
            key = "%s" % (week.week_type,)
            patterns = tbv1data.workout_patterns[key]

        try:
            key = "%s-%s" % (week.week_type, week.week_type_num)
            hpatterns = tbv1data.hour_patterns[key]
        except KeyError:
            key = "%s" % (week.week_type,)
            hpatterns = tbv1data.hour_patterns[key]

        week_hours = tbv1data.weekly_hours_lookup[week.weekly_hours()]
        start_index = (int(week.week_start_date.strftime("%w")) - 1) % 7

        entries = []
        for dow in range(0, 7):
            dow_ind = (dow + start_index) % 7
            wotype = patterns[dow_ind][0]

            # if dow not in entry_by_orig:
            entries.append(
                dict(
                    dow=dow,
                    workout_type=wotype,
                    scheduled_dow=dow_ind,
                    scheduled_length=week_hours[hpatterns[dow_ind] - 1],
                    actual_length=week_hours[hpatterns[dow_ind] - 1],
                )
            )

        return entries

    def workout_description(self, wo_type):
        return tbv1data.workouts[wo_type]

    def workout_types(self, entry):
        try:
            key = "%s-%s" % (entry.week.week_type, entry.week.week_type_num)
            patterns = tbv1data.workout_patterns[key]
        except KeyError:
            key = "%s" % (entry.week.week_type,)
            patterns = tbv1data.workout_patterns[key]

        # hours = tbv1data.weekly_hours_lookup[entry.week.weekly_hours()][entry.scheduled_dow]
        return patterns[entry.scheduled_dow]
