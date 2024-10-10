import { LoadingOverlay } from '@mantine/core';
import { Link } from 'react-router-dom';
import { useSeasonsList } from '../api/api-fetch';

export const TrainingPlans = () => {
  const { data: seasonData, isLoading } = useSeasonsList({});
  console.log('season', seasonData);
  return (
    <div>
      <LoadingOverlay visible={isLoading} zIndex={1000} overlayProps={{ radius: 'sm', blur: 2 }} />
      {seasonData && seasonData.count === 0 ? <Link to="/training/manage/add">Set up a training plan</Link> : null}
    </div>
  );
};
