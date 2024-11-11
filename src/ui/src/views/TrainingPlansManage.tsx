import { useNavigate, useParams } from 'react-router';
import { Button, NativeSelect, Stack } from '@mantine/core';
import { useEffect, useState } from 'react';
import { DateInput } from '@mantine/dates';
import { DateTime } from 'luxon';
import { TrainingEntryOut } from '../api/DTOs';
import { Calendar } from '../components/Calendar';
import { calendarDateOffset } from '../utils/dates';
import { api } from '../api/api-fetch';
import { FixedModal } from '../components/FixedModal';

const fixDate = (date: Date | null): Date | null => {
  if (date === null) {
    return null;
  }
  return calendarDateOffset(DateTime.fromJSDate(date), 0, -1).toJSDate();
};

const fetchPreview = async (annual_hours: number, season_start_date: Date | null, season_end_date: Date | null) => {
  return api.seasons.seasonsPreviewTrainingBibleV1({
    params: { annual_hours },
    season_start_date: season_start_date ? DateTime.fromJSDate(season_start_date).toISODate() || null : null,
    season_end_date: season_end_date ? DateTime.fromJSDate(season_end_date).toISODate() || null : null,
  });
};

export const TrainingPlanForm = () => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);
  const [annualHours, setAnnualHours] = useState<number>(200);
  const [annualHourChoices, setAnnualHourChoices] = useState<number[]>([]);
  const [entries, setEntries] = useState<TrainingEntryOut[]>([]);
  const [saving, setSaving] = useState<boolean>(false);

  useEffect(() => {
    const fetchData = async () => {
      const { data } = await fetchPreview(annualHours, startDate, endDate);
      setAnnualHourChoices(data.hour_selection);
      setEntries(data.entries);
    };

    if (startDate) {
      fetchData().then(_ => {});
    }
  }, [startDate, endDate, annualHours]);

  const firstDate = entries.map(e => DateTime.fromISO(e.entry_date)).sort()[0];
  const lastDate = entries
    .map(e => DateTime.fromISO(e.entry_date))
    .sort()
    .reverse()[0];

  console.log({ firstDate, lastDate });

  return (
    <Stack>
      <DateInput clearable value={startDate} onChange={date => setStartDate(fixDate(date))} label="Start date" placeholder="Start date" />
      <DateInput clearable value={endDate} onChange={setEndDate} label="End date (optional)" placeholder="End date" />
      <NativeSelect
        label="Yearly Hours"
        data={annualHourChoices.map(h => String(h))}
        onChange={event => setAnnualHours(Number(event.currentTarget.value))}
      />
      <Button
        disabled={!entries || entries.length === 0 || saving}
        onClick={async () => {
          setSaving(true);
          try {
            await api.trainingWeeks.trainingWeeksPopulate({
              season_start_date: firstDate.toISODate() || null,
              season_end_date: lastDate.toISODate() || null,
              training_plan: 'CTB',
              params: { annual_hours: annualHours },
            });
          } catch (e) {
            console.error(e);
          }
          setSaving(false);
        }}
      >
        Save plan
      </Button>
      <br />
      {entries && entries.length > 0 && <Calendar activities={[]} trainingEntries={entries} firstDate={firstDate} lastDate={lastDate} />}
    </Stack>
  );
};

export const TrainingPlansManage = () => {
  const navigate = useNavigate();
  const { command } = useParams();

  return (
    <FixedModal size="auto" opened={command === 'add'} onClose={() => navigate('/training')} title="Create new Training Plan Season">
      <TrainingPlanForm />
    </FixedModal>
  );
};
