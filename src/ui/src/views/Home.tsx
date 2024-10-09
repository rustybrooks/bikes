import { useState } from 'react';
import { DateTime } from 'luxon';
import { useActivitiesList } from '../api/api-fetch';
import { Calendar } from '../components/Calendar';

const calendarDateOffset = (offsetDays: number, adjust: number) => {
  let targetDate = DateTime.now().plus({ days: offsetDays });
  while (targetDate.weekdayLong !== 'Saturday') {
    targetDate = targetDate.plus({ days: adjust });
  }
  return targetDate;
};

export const Home = () => {
  const [firstDate] = useState(calendarDateOffset(-28, -1));
  const [lastDate] = useState(calendarDateOffset(0, 1).plus({ days: -1 }));
  const { data: activityData, isLoading } = useActivitiesList({
    start_datetime_local__gte: firstDate.toISO(),
    start_datetime_local__lte: lastDate.toISO(),
  });

  console.log('Ad!', activityData);

  return (
    <div>
      <Calendar activities={activityData?.results || []} firstDate={firstDate} lastDate={lastDate} />
    </div>
  );
};
