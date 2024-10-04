import { useCallback, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { apiFetch, apiUrl } from '../api/api-fetch';

const callback = async (code: string | null) => {
  const body = JSON.stringify({ code });
  console.log('body!', { body });
  const resp = await apiFetch(apiUrl('USERS_STRAVA_CALLBACK'), {
    method: 'POST',
    body,
  });

  console.log('resp', { resp });
};

export const StravaCallback = () => {
  const [searchParams] = useSearchParams();
  console.log('Stravacallback', searchParams);

  useEffect(() => {
    console.log('usecallback');
    callback(searchParams.get('code'));
  }, []);
  return <div>SC</div>;
};
