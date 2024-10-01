import useSWR, { KeyedMutator } from 'swr';
import { BASE_URL } from '../constants/api';

export const apiRoutes = {
  USERS_LOGIN: () => `api/users/login/`,
  USERS_SIGNUP: () => `api/users/signup/`,
};

export class UnauthenticatedError extends Error {
  constructor(msg: string) {
    super(msg);

    // Set the prototype explicitly.
    Object.setPrototypeOf(this, UnauthenticatedError.prototype);
  }
}

export const apiUrl = (apiRoute: keyof typeof apiRoutes) => {
  return `${BASE_URL}/${apiRoutes[apiRoute]()}`;
};

export const apiFetch = async (url: string, options: Record<string, unknown>) => {
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

  return res.json();
};

export const useUrl = <T>(
  apiRoute: keyof typeof apiRoutes,
  key: string | object | null = null,
  options: Record<string, unknown> = {},
): {
  data: T;
  isLoading: boolean;
  isError: boolean;
  mutate: KeyedMutator<unknown>;
  isUnauthenticated: boolean;
} => {
  const url = apiUrl(apiRoute);
  const { data, error, mutate } = useSWR([url, key || ''], () => apiFetch(url, options), {
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

// type ApiListCountResponse<T> = {
//   items: T[];
//   count: number;
// };

// export const useUsersMe = () => useUrl<MeResponse>('USERS_ME');
// export const useUsersLogout = () => useUrl<MeResponse>('USERS_LOGOUT');
// export const useUsersTokenExchange = (code: string, body: TokenExchangeIn) =>
//   useUrl<TokenExchangeOut>('USERS_TOKEN_EXCHANGE', code, { method: 'POST', body: JSON.stringify(body) });
// export const useAgentsList = () => useUrl<ApiListCountResponse<AgentOut>>('AGENTS_LIST');
// export const useRepositoriesList = () => useUrl<ApiListCountResponse<RepositoryOut>>('REPOSITORIES_LIST');
// export const useAlertsList = () => useUrl<ApiListCountResponse<AlertOut>>('ALERTS_LIST');
