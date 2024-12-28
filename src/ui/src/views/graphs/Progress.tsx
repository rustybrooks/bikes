import { AreaChart } from '@mantine/charts';
import { Group, Loader, SegmentedControl, Stack } from '@mantine/core';
import { DateTime } from 'luxon';
import { useState } from 'react';
import { IconBalloon } from '@tabler/icons-react';
import { useGraphsProgress } from '../../api/api-fetch';
import { METER_TO_MILE } from '../../constants/metrics';
import { icons } from '../../constants/icons';

export const toXaxis = (timestamp: string): number => {
  return DateTime.fromISO(timestamp).ordinal;
};

const colors = [
  'red.6',
  'pink.6',
  'grape.6',
  'violet.6',
  'indigo.6',
  'blue.6',
  'cyan.6',
  'teal.6',
  'green.6',
  'lime.6',
  'yellow.6',
  'orange.6',
];

export const Progress = () => {
  const [workoutType, setWorkoutType] = useState<string | null>(null);
  const [measureType, setMeasureType] = useState<string>('time');

  const { data, isLoading } = useGraphsProgress({
    // start_date: '2015-01-01',
    workout_type: workoutType === 'All' ? null : workoutType,
  });

  if (isLoading || !data) {
    return <Loader />;
  }

  console.log('data!', data);
  const series = data
    .map(ser => ser.year)
    .map((year, i) => ({
      name: String(year),
      color: colors[i % colors.length],
    }));

  const xaxis = Array.from(
    data.reduce((prev: Set<number>, next) => {
      return prev.union(new Set(next.data.map(d => toXaxis(d.timestamp))));
    }, new Set() as Set<number>),
  );
  xaxis.sort();

  const graphData: Record<string, Record<string, any>> = Object.fromEntries(xaxis.map(ts => [ts, { date: ts }]));
  console.log({ xaxis, series, graphData });
  data.forEach(d => {
    d.data.forEach(d2 => {
      graphData[toXaxis(d2.timestamp)][String(d.year)] = measureType === 'distance' ? d2.distance * METER_TO_MILE : d2.time / 3600;
    });
  });

  return (
    <Stack>
      <Group>
        <SegmentedControl
          data={[
            {
              value: 'All',
              label: <IconBalloon size="2rem" />,
            },
            {
              value: 'Ride',
              label: <icons.ride size="2rem" />,
            },
            {
              value: 'Run',
              label: <icons.run size="2rem" />,
            },
            {
              value: 'Walk',
              label: <icons.walk size="2rem" />,
            },
          ]}
          value={workoutType ?? undefined}
          fullWidth={false}
          onChange={setWorkoutType}
          color="blue"
        />

        <span>{'  '}</span>

        <SegmentedControl
          data={[
            { value: 'time', label: 'Time' },
            { value: 'distance', label: 'Distance' },
          ]}
          value={measureType ?? undefined}
          fullWidth={false}
          onChange={setMeasureType}
          color="blue"
        />
      </Group>
      <AreaChart
        h={300}
        withDots={false}
        withLegend={true}
        data={Object.values(graphData)}
        dataKey="date"
        series={series}
        curveType="linear"
        valueFormatter={value => value.toFixed(1)}
      />
    </Stack>
  );
};
