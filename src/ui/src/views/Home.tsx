import { useState } from 'react';
import { LoadingOverlay } from '@mantine/core';
import { DateTime } from 'luxon';
import { useActivitiesList, useTrainingEntriesList, useTrainingWeeksList } from '../api/api-fetch';
import { Calendar } from '../components/Calendar';
import { calendarDateOffset } from '../utils/dates';

export const Home = () => {
  const [firstDate] = useState(calendarDateOffset(DateTime.now(), -28, -1));
  const [lastDate] = useState(calendarDateOffset(DateTime.now(), 0, 1).plus({ days: -1 }));
  const { data: activityData, isLoading } = useActivitiesList({
    ...(firstDate ? { start_datetime_local__gte: firstDate.toISO() || '' } : null),
    ...(lastDate ? { start_datetime_local__lte: lastDate.toISO() || '' } : null),
  });
  const { data: entriesData, isLoading: isLoading2 } = useTrainingEntriesList({
    ...(firstDate ? { week__week_start_date__gte: firstDate.toISODate() || '' } : null),
    ...(lastDate ? { week__week_start_date__lte: lastDate.toISODate() || '' } : null),
  });

  return (
    <div>
      <LoadingOverlay visible={isLoading || isLoading2} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      <Calendar
        activities={activityData?.results || []}
        trainingEntries={entriesData?.results || []}
        firstDate={firstDate}
        lastDate={lastDate}
      />
    </div>
  );
};
