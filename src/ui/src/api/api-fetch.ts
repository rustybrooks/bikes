import useSWR, { KeyedMutator } from 'swr';
import { BASE_URL } from '../constants/api';
import { ActivityOut, Season } from './DTOs';

export const apiRoutes = {
  USERS_LOGIN: () => `api/users/login/`,
  USERS_SIGNUP: () => `api/users/signup/`,
  USERS_STRAVA_CALLBACK: () => `api/users/strava_callback/`,
  ACTIVITIES_LIST: (params: Record<string, any>) => `api/activities/?${new URLSearchParams(params).toString()}`,
  // ACTIVITIES_READ: (activityId: number | string) => `api/activities/${activityId}/`,
  SEASONS_LIST: (params: Record<string, any>) => `api/seasons/?${new URLSearchParams(params).toString()}`,
  SEASONS_CTB_PREVIEW: () => `api/seasons/preview_training_bible_v1/`,
};

export class UnauthenticatedError extends Error {
  constructor(msg: string) {
    super(msg);

    // Set the prototype explicitly.
    Object.setPrototypeOf(this, UnauthenticatedError.prototype);
  }
}

export const apiUrl = (apiRoute: keyof typeof apiRoutes) => {
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  // @ts-expect-error
  return (...args: any[]) => `${BASE_URL}/${apiRoutes[apiRoute](...args)}`;
};

export const apiFetch = async <T>(url: string, options: Record<string, unknown>) => {
  // const tokens: UserTokens | null = JSON.parse(localStorage.getItem(userStorageKey) || '{}');

  const headers = {
    ...(options?.headers || {}),
    'content-type': 'application/json',
  };

  const res = await fetch(url, {
    ...options,
    credentials: 'include', // this is required in order for cross-site cookies to work
    headers,
  });
  if (!res.ok) {
    if (res.status === 401) {
      throw new UnauthenticatedError('Unauthenticated');
    }
    throw new Error('An error occurred while fetching the data.');
  }

  return res.json() as T;
};

export const useUrl = <T>(
  url: string,
  key: string | object | null = null,
  options: Record<string, unknown> = {},
): {
  data: T | undefined;
  isLoading: boolean;
  isError: boolean;
  mutate: KeyedMutator<T>;
  isUnauthenticated: boolean;
} => {
  // console.log('useUrl', { url, key, options });
  const { data, error, mutate } = useSWR([url, key || ''], () => apiFetch<T>(url, options), {
    revalidateOnFocus: false,
    revalidateIfStale: false,
  });

  return {
    data,
    isLoading: !error && !data,
    mutate,
    isError: !!error,
    isUnauthenticated: error instanceof UnauthenticatedError,
  };
};

// function useFetch<T>(
//   url,
//   options: Record<string, unknown> = {},
// ): {
//   data: T;
//   loading: boolean;
//   error: any;
// } {
//   const [data, setData] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);
//
//   useEffect(() => {
//     setLoading(true);
//     setData(null);
//     setError(null);
//
//     const headers = {
//       ...(options?.headers || {}),
//       'content-type': 'application/json',
//     };
//
//     fetch(url, {
//       ...options,
//       credentials: 'include', // this is required in order for cross-site cookies to work
//       headers,
//     })
//       .then(res => {
//         setLoading(false);
//         // checking for multiple responses for more flexibility
//         // with the url we send in.
//         if (res.body) setData(res.json() as T);
//       })
//       .catch(err => {
//         setLoading(false);
//         setError(err);
//       });
//   }, [url]);
//
//   return { data, loading, error };
// }

type ApiListCountResponse<T> = {
  results: T[];
  count: number;
};

export const useActivitiesList = (params: Record<string, any>) =>
  useUrl<ApiListCountResponse<ActivityOut>>(apiUrl('ACTIVITIES_LIST')(params));
// export const useActivity = (activityId: string) => useUrl<ActivityOut>(apiUrl('ACTIVITIES_READ')(activityId));
export const useSeasonsList = (params: Record<string, any>) => useUrl<ApiListCountResponse<Season>>(apiUrl('SEASONS_LIST')(params));
