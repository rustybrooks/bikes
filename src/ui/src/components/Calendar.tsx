import { Box, Card, Center, Grid, Group, HoverCard, LoadingOverlay, Stack, Text } from '@mantine/core';
import { IconDeviceUnknown, IconRun, IconWalk, IconReceipt } from '@tabler/icons-react';
import { DateTime, Interval } from 'luxon';

import { Link } from 'react-router-dom';
import classes from './Calendar.module.css';
import { ActivityOut, TrainingEntryOut } from '../api/DTOs';
import { chunkArray } from '../utils/arrays';
import { METER_TO_MILE } from '../constants/metrics';
import { icons } from '../constants/icons';

const formatSecondsTime = (sec: number): string => {
  const date = new Date(0);
  date.setSeconds(sec); // specify value for SECONDS here
  return date.toISOString().substring(11, 19);
};

const actIcon = (type: string, color = 'white') => {
  switch (type) {
    case 'Ride':
      return <icons.ride stroke={1.5} size="1rem" style={{ color }} />;
    case 'Walk':
      return <icons.walk stroke={1.5} size="1rem" style={{ color }} />;
    case 'Run':
      return <icons.run stroke={1.5} size="1rem" style={{ color }} />;
    case 'total':
      return <IconReceipt stroke={1.5} size="1rem" style={{ color }} />;
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
          <Link to={`activity/${activity.activity_id}`} style={{ color: 'white' }}>
            <Group gap="5px" justify="space-between" className={classes.exercisename}>
              <Text size="sm">{(activity.distance * METER_TO_MILE).toFixed(1)}mi</Text>
              <Box w={70}>
                <Text size="xs" truncate>
                  {activity.activity_name}
                </Text>
              </Box>
              {actIcon(activity.type, 'white')}
            </Group>
          </Link>
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

export const WeekSummaryCard = ({ dates, calendar }: { dates: string[]; calendar: Record<string, CalendarEntry> }) => {
  const weeklyActivityHours: Record<string, number> = { total: 0 };
  const weeklyTrainingHours: Record<string, number> = { total: 0 };
  dates.forEach(date => {
    calendar[date].activities.forEach(activity => {
      if (!(activity.type in weeklyActivityHours)) {
        weeklyActivityHours[activity.type] = 0;
      }

      weeklyActivityHours[activity.type] += activity.moving_time / 3600;
      weeklyActivityHours.total += activity.moving_time / 3600;
    });

    calendar[date].trainingEntries.forEach(activity => {
      if (!(activity.activity_type in weeklyTrainingHours)) {
        weeklyTrainingHours[activity.activity_type] = 0;
      }
      weeklyTrainingHours[activity.activity_type] += activity.scheduled_length;
      weeklyTrainingHours.total += activity.scheduled_length;
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
                  {(weeklyActivityHours[key] || 0).toFixed(1)} / {(weeklyTrainingHours[key] || 0).toFixed(1)}
                </Text>
              </Group>
            );
          })}
        </Stack>
      </Card.Section>
    </Card>
  );
};

export const TrainingEntryCard = ({ entry }: { entry: TrainingEntryOut }) => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  const details = entry.workout_types[entry.workout_type] || [];
  return (
    <Card>
      <Text>
        <b>{details[0]}</b>
      </Text>
      <Text>{details[1]}</Text>
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

        {weekChunks.map((week, wi) => {
          return [
            ...week.map((date, di) => {
              const ld = DateTime.fromISO(date);
              return (
                <Grid.Col span={1} key={date}>
                  <Card key={date} className={classes.day} padding="xs">
                    <Card.Section withBorder={false} inheritPadding py="xs">
                      <Box>
                        {(calendar[date].trainingEntries || []).map(entry => (
                          <HoverCard key={entry.id} width={400} position="bottom" withArrow shadow="md" openDelay={250}>
                            <HoverCard.Target>
                              <Text span className="workout" size={'sm'}>
                                {entry.workout_type} | {entry.scheduled_length}
                              </Text>
                            </HoverCard.Target>
                            <HoverCard.Dropdown>
                              <TrainingEntryCard entry={entry} />
                            </HoverCard.Dropdown>
                          </HoverCard>
                        ))}
                        <span className={classes.date}>
                          {(wi === 0 && di === 0) || ld.day === 1 ? (
                            <Text c="#999" span>
                              {ld.monthShort}
                            </Text>
                          ) : null}
                          &nbsp;
                          <Text span>{date.split('-')[2]}</Text>
                        </span>
                      </Box>
                    </Card.Section>
                    <Stack>
                      {(calendar[date].activities || []).map(act => (
                        <ActivityCard activity={act} key={act.activity_id} />
                      ))}
                    </Stack>
                  </Card>
                </Grid.Col>
              );
            }),
            <Grid.Col span={1} key="summary">
              <WeekSummaryCard dates={week} calendar={calendar} key={week[0]} />
            </Grid.Col>,
          ];
        })}
      </Grid>
    </Box>
  );
};
