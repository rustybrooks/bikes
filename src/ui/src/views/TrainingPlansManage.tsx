import { useNavigate, useParams } from 'react-router';
import { Modal, NativeSelect } from '@mantine/core';
import { useState } from 'react';
import { DateInput } from '@mantine/dates';
import { DateTime } from 'luxon';
import { apiFetch, apiUrl } from '../api/api-fetch';

const fetchPreview = async (annual_hours: string, season_start_date: Date | null, season_end_date: Date | null) => {
  const body = JSON.stringify({
    annual_hours: Number(annual_hours),
    season_start_date: season_start_date ? DateTime.fromJSDate(season_start_date).toISODate() : null,
    season_end_date: season_end_date ? DateTime.fromJSDate(season_end_date).toISODate() : null,
  });

  apiFetch(apiUrl('SEASONS_CTB_PREVIEW')(), {
    method: 'POST',
    body,
  });
};

export const TrainingPlanForm = () => {
  const [startDate, setStartDate] = useState<Date | null>(null);
  const [endDate, setEndDate] = useState<Date | null>(null);

  console.log(endDate, startDate);

  return (
    <div>
      <DateInput
        clearable
        value={startDate}
        onChange={value => {
          setStartDate(value);
          fetchPreview('200', startDate, endDate);
        }}
        label="Date input"
        placeholder="Date input"
      />
      <DateInput
        clearable
        value={endDate}
        onChange={value => {
          setEndDate(value);
          fetchPreview('200', startDate, endDate);
        }}
        label="Date input"
        placeholder="Date input"
      />
      <NativeSelect label="Yearly Hours" data={['200']} />
      {/* <Calendar /> */}
    </div>
  );
};

export const TrainingPlansManage = () => {
  const navigate = useNavigate();
  const { command } = useParams();
  return (
    <div>
      <Modal opened={command === 'add'} onClose={() => navigate('/training')} title="Create new Training Plan Season">
        <TrainingPlanForm />
      </Modal>
    </div>
  );
};
