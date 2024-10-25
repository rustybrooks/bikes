import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { api } from '../api/api-fetch';

const callback = async (code: string | null) => {
  const body = JSON.stringify({ code });
  console.log('body!', { body });
  const resp = await api.users.usersStravaCallback({ code });

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
