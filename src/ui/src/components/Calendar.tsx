import { Box, Card, Center, Grid, Group, LoadingOverlay, Stack, Text } from '@mantine/core';
import { IconBike, IconDeviceUnknown, IconRun, IconWalk } from '@tabler/icons-react';
import { DateTime, Interval } from 'luxon';

import classes from './Calendar.module.css';
import { ActivityOut } from '../api/DTOs';

const METER_TO_MILE = 0.6 / 1000;

const formatSecondsTime = (sec: number): string => {
  const date = new Date(0);
  date.setSeconds(sec); // specify value for SECONDS here
  return date.toISOString().substring(11, 19);
};

const actIcon = (type: string) => {
  switch (type) {
    case 'Ride':
      return <IconBike stroke={1.5} size="1rem" className={classes.icon} />;
    case 'Walk':
      return <IconWalk stroke={1.5} size="1rem" className={classes.icon} />;
    case 'Run':
      return <IconRun stroke={1.5} size="1rem" className={classes.icon} />;
    default:
      return <IconDeviceUnknown stroke={1.5} size="1rem" className={classes.icon} />;
  }
};

type CalendarEntry = {
  activities: ActivityOut[];
};

export const Calendar = ({ activities, firstDate, lastDate }: { activities: ActivityOut[]; firstDate: DateTime; lastDate: DateTime }) => {
  const dow = ['Sat', 'Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri'];

  const calendar: Record<string, CalendarEntry> = Object.fromEntries(
    Interval.fromDateTimes(firstDate.startOf('day'), lastDate.endOf('day'))
      .splitBy({ day: 1 })
      .map((date: Interval) => [(date.start || DateTime.now()).toISODate(), { activities: [] }]),
  );

  activities.forEach(activity => {
    const localStart = DateTime.fromISO(activity.start_datetime || '');
    calendar[localStart.toISODate() || ''].activities.push(activity);
  });

  return (
    <>
      <LoadingOverlay visible={!calendar} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      <Grid columns={7}>
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

        {Object.keys(calendar).map(date => (
          <Grid.Col span={1} key={date}>
            <Card key={date} className={classes.day} padding="xs">
              <Card.Section withBorder={false} inheritPadding py="xs">
                <Text className={classes.date}>{date.split('-')[2]}</Text>
              </Card.Section>
              <Stack>
                {(calendar[date].activities || []).map(act => {
                  return (
                    <Card withBorder={true} key={act.activity_id} padding="xs">
                      <Card.Section>
                        <Box className={classes.exerciseheader}>
                          <Group gap="xs" justify="space-between" className={classes.exercisename}>
                            <Box w="7rem" component="span">
                              <Text size="sm" truncate="end">
                                {act.activity_name}&nbsp;
                              </Text>
                            </Box>
                            <Text size="sm">{(act.distance * METER_TO_MILE).toFixed(1)}mi</Text> {actIcon(act.type)}
                          </Group>
                        </Box>
                      </Card.Section>

                      <Group justify="space-between">
                        <Text span size={'sm'}>
                          {formatSecondsTime(act.moving_time)}
                        </Text>

                        <Text span size={'sm'}>
                          {(3600 * (act.average_speed || 0) * METER_TO_MILE).toFixed(1)}mph
                        </Text>
                      </Group>
                      <Group justify="space-between">
                        <Text span size={'sm'}>
                          {(act.kilojoules || 0).toFixed(0)}kJ
                        </Text>
                        <Text span size={'sm'}>
                          {(act.average_watts || 0).toFixed(0)}w
                        </Text>
                      </Group>
                    </Card>
                  );
                })}
              </Stack>
            </Card>
          </Grid.Col>
        ))}
      </Grid>
    </>
  );
};
