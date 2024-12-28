/* eslint-disable @typescript-eslint/no-explicit-any */

import useSWR, { KeyedMutator } from 'swr';
import { Api, HttpResponse } from './DTOs';
import { BASE_URL } from '../constants/api';

type UnwrapHttpResponse<T extends HttpResponse<any>> = T extends HttpResponse<infer U> ? U : never;

export const api = new Api({
  baseUrl: `${BASE_URL}/api`,
  baseApiParams: {
    headers: {
      authorization: '',
    },
    credentials: 'include',
  },
});

export const fetchWrapper = async <
  FetchReturnType extends Awaited<Promise<PromiseLike<ReturnType<FetchFnType>>>>,
  FetchFnType extends (...args: any[]) => Promise<HttpResponse<FetchReturnType>>,
>(
  args: any[],
  fetchFn: FetchFnType,
): Promise<UnwrapHttpResponse<FetchReturnType>> => {
  const r = await fetchFn(...args);
  if (r.error) {
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw r.error;
  }

  return r.data as UnwrapHttpResponse<FetchReturnType>;
};

export const createUseUrl = <
  FetchReturnType extends Awaited<Promise<PromiseLike<ReturnType<FetchFnType>>>>,
  FetchFnType extends (...args: any[]) => Promise<HttpResponse<FetchReturnType>>,
>(
  fetchFn: FetchFnType,
  swrOptions: Record<string, boolean | number> | null = null,
) => {
  const allSwrOptions = {
    revalidateOnFocus: false,
    revalidateIfStale: false,
    revalidateOnMount: true,
    revalidateOnError: true,
    revalidateOnReconnect: true,
    ...swrOptions,
  };

  return (
    ...fetchArgs: Parameters<FetchFnType>
  ): {
    data: UnwrapHttpResponse<FetchReturnType> | undefined;
    isLoading: boolean;
    isError: boolean;
    mutate: KeyedMutator<UnwrapHttpResponse<FetchReturnType>>;
    error: any;
  } => {
    const { data, error, mutate } = useSWR<UnwrapHttpResponse<FetchReturnType>>(
      [fetchFn, ...fetchArgs],
      () => fetchWrapper(fetchArgs, fetchFn),
      allSwrOptions,
    );

    return {
      data,
      isLoading: !error && !data,
      mutate,
      isError: !!error,
      error,
    };
  };
};

export const useActivitiesList = createUseUrl(api.activities.activitiesList);
export const useSeasonsList = createUseUrl(api.seasons.seasonsList);
export const useTrainingEntriesList = createUseUrl(api.trainingEntries.trainingEntriesList);
export const useActivityRead = createUseUrl(api.activities.activitiesRead);
// export const useTrainingWeeksList = createUseUrl(api.trainingWeeks.trainingWeeksList);

export const useGraphsProgress = createUseUrl(api.graphs.graphsProgress);
