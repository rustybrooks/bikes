import { useState } from 'react';
import { LoadingOverlay } from '@mantine/core';
import { DateTime } from 'luxon';
import { useActivitiesList } from '../api/api-fetch';
import { Calendar } from '../components/Calendar';
import { calendarDateOffset } from '../utils/dates';

export const Home = () => {
  const [firstDate] = useState(calendarDateOffset(DateTime.now(), -28, -1));
  const [lastDate] = useState(calendarDateOffset(DateTime.now(), 0, 1).plus({ days: -1 }));
  const { data: activityData, isLoading } = useActivitiesList({
    ...(firstDate ? { start_datetime_local__gte: firstDate.toISO() || '' } : null),
    ...(lastDate ? { start_datetime_local__lte: lastDate.toISO() || '' } : null),
  });

  return (
    <div>
      <LoadingOverlay visible={isLoading} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      <Calendar activities={activityData?.results || []} trainingEntries={[]} firstDate={firstDate} lastDate={lastDate} />
    </div>
  );
};
