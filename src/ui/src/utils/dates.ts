import { DateTime } from 'luxon';

export const calendarDateOffset = (targetDate: DateTime, offsetDays: number, adjust: number) => {
  // eslint-disable-next-line no-param-reassign
  targetDate = targetDate.plus({ days: offsetDays });
  while (targetDate.weekdayLong !== 'Saturday') {
    // eslint-disable-next-line no-param-reassign
    targetDate = targetDate.plus({ days: adjust });
  }
  return targetDate;
};
