import { useState } from 'react';
import { DateTime } from 'luxon';
import { useActivitiesList } from '../api/api-fetch';

const calendarDateOffset = (offsetDays: number) => {
  let targetDate = DateTime.now().plus({ days: offsetDays });
  while (targetDate.weekdayLong !== 'Saturday') {
    console.log(targetDate, targetDate.weekdayLong);
    targetDate = targetDate.plus({ days: -1 });
  }
  return targetDate;
};

export const Home = () => {
  const [firstDate] = useState(calendarDateOffset(-30));
  const [lastDate] = useState(calendarDateOffset(0));
  const { data, isLoading } = useActivitiesList({
    start_datetime_local__gte: firstDate.toISO(),
    start_datetime_local__lte: lastDate.toISO(),
  });

  if (isLoading) {
    return <div>Welcome to bikes!</div>;
  }
  console.log(data);
  return <div>foo</div>;
};
