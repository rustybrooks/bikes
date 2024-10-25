import { Box, Card, Center, Grid, Group, LoadingOverlay, Stack, Text } from '@mantine/core';
import { IconBike, IconDeviceUnknown, IconRun, IconWalk } from '@tabler/icons-react';
import { DateTime, Interval } from 'luxon';

import classes from './Calendar.module.css';
import { ActivityOut, TrainingEntryOut } from '../api/DTOs';
import { chunkArray } from '../utils/arrays';

const METER_TO_MILE = 0.6 / 1000;

const formatSecondsTime = (sec: number): string => {
  const date = new Date(0);
  date.setSeconds(sec); // specify value for SECONDS here
  return date.toISOString().substring(11, 19);
};

const actIcon = (type: string, color = 'white') => {
  switch (type) {
    case 'Ride':
      return <IconBike stroke={1.5} size="1rem" style={{ color }} />;
    case 'Walk':
      return <IconWalk stroke={1.5} size="1rem" style={{ color }} />;
    case 'Run':
      return <IconRun stroke={1.5} size="1rem" style={{ color }} />;
    default:
      return <IconDeviceUnknown stroke={1.5} size="1rem" style={{ color }} />;
  }
};

type CalendarEntry = {
  activities: ActivityOut[];
  trainingEntries: TrainingEntryOut[];
};

export const ActivityCard = ({ activity }: { activity: ActivityOut }) => {
  return (
    <Card withBorder={true} padding="xs">
      <Card.Section>
        <Box className={classes.exerciseheader}>
          <Group gap="xs" justify="space-between" className={classes.exercisename}>
            <Text size="sm">{(activity.distance * METER_TO_MILE).toFixed(1)}mi</Text>
            {actIcon(activity.type, 'white')}
          </Group>
        </Box>
      </Card.Section>

      <Group justify="space-between">
        <Text span size={'sm'}>
          {formatSecondsTime(activity.moving_time)}
        </Text>

        <Text span size={'sm'}>
          {(3600 * (activity.average_speed || 0) * METER_TO_MILE).toFixed(1)}mph
        </Text>
      </Group>
      <Group justify="space-between">
        <Text span size={'sm'}>
          {(activity.kilojoules || 0).toFixed(0)}kJ
        </Text>
        <Text span size={'sm'}>
          {(activity.average_watts || 0).toFixed(0)}w
        </Text>
      </Group>
    </Card>
  );
};

export const TrainingCard = ({ entry }: { entry: TrainingEntryOut }) => {
  return (
    <Card withBorder={true} padding="xs">
      <Card.Section>
        <Box className={classes.exerciseheader}>
          <Group gap="xs" justify="space-between" className={classes.exercisename}>
            <Text size="sm" truncate="end">
              {entry.workout_type}&nbsp;
            </Text>
          </Group>
        </Box>
      </Card.Section>

      <Group justify="space-between"></Group>
    </Card>
  );
};

export const WeekSummaryCard = ({ dates, calendar }: { dates: string[]; calendar: Record<string, CalendarEntry> }) => {
  const weeklyActivityHours: Record<string, number> = {};
  const weeklyTrainingHours: Record<string, number> = {};
  dates.forEach(date => {
    calendar[date].activities.forEach(activity => {
      if (!(activity.type in weeklyActivityHours)) {
        weeklyActivityHours[activity.type] = 0;
      }

      weeklyActivityHours[activity.type] += activity.moving_time;
    });

    calendar[date].trainingEntries.forEach(activity => {
      if (!(activity.activity_type in weeklyTrainingHours)) {
        weeklyTrainingHours[activity.activity_type] = 0;
      }
      weeklyTrainingHours[activity.activity_type] += activity.scheduled_length;
    });
  });

  const allKeys = new Set([...Object.keys(weeklyActivityHours), ...Object.keys(weeklyTrainingHours)]);

  return (
    <Card className={classes.day} padding="xs">
      <Card.Section withBorder={false} inheritPadding py="xs">
        <Stack>
          {[...allKeys].sort().map(key => {
            return (
              <Group key={key}>
                {actIcon(key, 'black')}
                <Text span size="sm">
                  {((weeklyActivityHours[key] || 0) / 3600).toFixed(1)} / {((weeklyTrainingHours[key] || 0) / 3600).toFixed(1)}
                </Text>
              </Group>
            );
          })}
        </Stack>
      </Card.Section>
    </Card>
  );
};

export const Calendar = ({
  activities,
  trainingEntries,
  firstDate,
  lastDate,
}: {
  activities: ActivityOut[];
  trainingEntries: TrainingEntryOut[];
  firstDate: DateTime;
  lastDate: DateTime;
}) => {
  const dow = ['Sat', 'Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri'];

  const calendar: Record<string, CalendarEntry> = Object.fromEntries(
    Interval.fromDateTimes(firstDate.startOf('day'), lastDate.endOf('day'))
      .splitBy({ day: 1 })
      .map((date: Interval) => [
        (date.start || DateTime.now()).toISODate(),
        {
          activities: [],
          trainingEntries: [],
        },
      ]),
  );

  const weekChunks = chunkArray(Object.keys(calendar), 7);

  activities.forEach(activity => {
    const localStart = DateTime.fromISO(activity.start_datetime || '');
    calendar[localStart.toISODate() || ''].activities.push(activity);
  });

  trainingEntries.forEach(trainingEntry => {
    const localStart = DateTime.fromISO(trainingEntry.entry_date || '');
    calendar[localStart.toISODate() || ''].trainingEntries.push(trainingEntry);
  });

  return (
    <Box style={{ background: '#eee' }}>
      <LoadingOverlay visible={!calendar} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      <Grid columns={8}>
        {dow.map(d => {
          return (
            <Grid.Col span={1} key={d}>
              <Card key={d} className={classes.header}>
                <Center>
                  <Text>{d}</Text>
                </Center>
              </Card>
            </Grid.Col>
          );
        })}

        <Grid.Col span={1} key="summary">
          <Card key="summary" className={classes.header}>
            <Center>
              <Text>Summary</Text>
            </Center>
          </Card>
        </Grid.Col>

        {weekChunks.map(week => {
          return [
            ...week.map(date => (
              <Grid.Col span={1} key={date}>
                <Card key={date} className={classes.day} padding="xs">
                  <Card.Section withBorder={false} inheritPadding py="xs">
                    <Box>
                      {(calendar[date].trainingEntries || []).map(entry => (
                        <Text span className="workout" size={'sm'}>
                          {entry.workout_type} | {entry.scheduled_length}
                        </Text>
                      ))}
                      <Text span className={classes.date}>
                        {date.split('-')[2]}
                      </Text>
                    </Box>
                  </Card.Section>
                  <Stack>
                    {/* {(calendar[date].trainingEntries || []).map(entry => ( */}
                    {/*  <TrainingCard entry={entry} key={entry.id} /> */}
                    {/* ))} */}
                    {(calendar[date].activities || []).map(act => (
                      <ActivityCard activity={act} key={act.activity_id} />
                    ))}
                  </Stack>
                </Card>
              </Grid.Col>
            )),
            <Grid.Col span={1} key="summary">
              <WeekSummaryCard dates={week} calendar={calendar} key={week[0]} />
            </Grid.Col>,
          ];
        })}
      </Grid>
    </Box>
  );
};
