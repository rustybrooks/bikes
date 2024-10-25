import { useNavigate, useParams } from 'react-router';
import { Modal, NativeSelect } from '@mantine/core';
import { useEffect, useState } from 'react';
import { DateInput } from '@mantine/dates';
import { DateTime } from 'luxon';
import { TrainingEntryOut } from '../api/DTOs';
import { Calendar } from '../components/Calendar';
import { calendarDateOffset } from '../utils/dates';
import { api } from '../api/api-fetch';

const fixDate = (date: Date | null): Date | null => {
  if (date === null) {
    return null;
  }
  return calendarDateOffset(DateTime.fromJSDate(date), 0, -1).toJSDate();
};

const fetchPreview = async (annual_hours: number, season_start_date: Date | null, season_end_date: Date | null) => {
  return api.seasons.seasonsPreviewTrainingBibleV1({
    annual_hours,
    season_start_date: season_start_date ? DateTime.fromJSDate(season_start_date).toISODate() : '',
    season_end_date: season_end_date ? DateTime.fromJSDate(season_end_date).toISODate() : '',
  });
};

export const TrainingPlanForm = () => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [yearlyHours, setYearlyHours] = useState<number>(200);
  const [yearlyHourChoices, setYearlyHourChoices] = useState<number[]>([]);
  const [entries, setEntries] = useState<TrainingEntryOut[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      const { data } = await fetchPreview(yearlyHours, startDate, endDate);
      setYearlyHourChoices(data.hour_selection);
      setEntries(data.entries);
    };

    fetchData();
  }, [startDate, endDate, yearlyHours]);

  const firstDate = entries.map(e => DateTime.fromISO(e.entry_date)).sort()[0];
  const lastDate = entries
    .map(e => DateTime.fromISO(e.entry_date))
    .sort()
    .reverse()[0];

  console.log({ firstDate, lastDate });

  return (
    <div>
      <DateInput clearable value={startDate} onChange={date => setStartDate(fixDate(date))} label="Start date" placeholder="Start date" />
      <DateInput clearable value={endDate} onChange={setEndDate} label="End date (optional)" placeholder="End date" />
      <NativeSelect
        label="Yearly Hours"
        data={yearlyHourChoices.map(h => String(h))}
        onChange={event => setYearlyHours(Number(event.currentTarget.value))}
      />
      {firstDate && lastDate && <Calendar activities={[]} trainingEntries={entries} firstDate={firstDate} lastDate={lastDate} />}
    </div>
  );
};

export const TrainingPlansManage = () => {
  const navigate = useNavigate();
  const { command } = useParams();
  return (
    <div>
      <Modal size="auto" opened={command === 'add'} onClose={() => navigate('/training')} title="Create new Training Plan Season">
        <TrainingPlanForm />
      </Modal>
    </div>
  );
};
