/* eslint-disable */
/* tslint:disable */
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface ActivityOut {
  /**
   * Activity id
   * @min -9223372036854776000
   * @max 9223372036854776000
   */
  activity_id: number;
  /**
   * External id
   * @minLength 1
   */
  external_id?: string | null;
  /**
   * Upload id
   * @min -9223372036854776000
   * @max 9223372036854776000
   */
  upload_id?: number | null;
  /**
   * Athlete id
   * @min -9223372036854776000
   * @max 9223372036854776000
   */
  athlete_id: number;
  /**
   * Activity name
   * @minLength 1
   */
  activity_name?: string | null;
  /** Distance */
  distance: number;
  /**
   * Moving time
   * @min -2147483648
   * @max 2147483647
   */
  moving_time: number;
  /**
   * Elapsed time
   * @min -2147483648
   * @max 2147483647
   */
  elapsed_time: number;
  /** Total elevation gain */
  total_elevation_gain: number;
  /** Elev high */
  elev_high?: number | null;
  /** Elev low */
  elev_low?: number | null;
  /**
   * Type
   * @minLength 1
   */
  type: string;
  /**
   * Start datetime
   * @format date-time
   */
  start_datetime?: string | null;
  /**
   * Start datetime local
   * @format date-time
   */
  start_datetime_local: string;
  /**
   * Timezone
   * @minLength 1
   */
  timezone: string;
  /** Start lat */
  start_lat?: number | null;
  /** Start long */
  start_long?: number | null;
  /** End lat */
  end_lat?: number | null;
  /** End long */
  end_long?: number | null;
  /**
   * Achievement count
   * @min -2147483648
   * @max 2147483647
   */
  achievement_count: number;
  /**
   * Athlete count
   * @min -2147483648
   * @max 2147483647
   */
  athlete_count: number;
  /** Trainer */
  trainer?: boolean;
  /** Commute */
  commute?: boolean;
  /** Manual */
  manual?: boolean;
  /** Private */
  private?: boolean;
  /**
   * Embed token
   * @minLength 1
   */
  embed_token?: string | null;
  /** Flagged */
  flagged?: boolean;
  /**
   * Workout type
   * @min -2147483648
   * @max 2147483647
   */
  workout_type?: number | null;
  /**
   * Gear id
   * @minLength 1
   */
  gear_id?: string | null;
  /** Average speed */
  average_speed?: number | null;
  /** Max speed */
  max_speed?: number | null;
  /** Average cadence */
  average_cadence?: number | null;
  /** Average temp */
  average_temp?: number | null;
  /** Average watts */
  average_watts?: number | null;
  /** Max watts */
  max_watts?: number | null;
  /** Weighted average watts */
  weighted_average_watts?: number | null;
  /** Kilojoules */
  kilojoules?: number | null;
  /** Device watts */
  device_watts?: boolean | null;
  /** Average heartrate */
  average_heartrate?: number | null;
  /** Max heartrate */
  max_heartrate?: number | null;
  /**
   * Suffer score
   * @min -2147483648
   * @max 2147483647
   */
  suffer_score?: number | null;
  /** User */
  user: number;
}

export interface Season {
  /** ID */
  id?: number;
  /** Training plan */
  training_plan: 'CTB' | 'TCC';
  /**
   * Season start date
   * @format date
   */
  season_start_date: string;
  /**
   * Season end date
   * @format date
   */
  season_end_date: string;
  /** Params */
  params: object;
  /** User */
  user: number;
}

export interface TrainingBibleV1In {
  /**
   * Season start date
   * @format date
   */
  season_start_date: string;
  /**
   * Season end date
   * @format date
   */
  season_end_date: string;
  /** Annual hours */
  annual_hours: number;
}

export interface TrainingEntryOut {
  /** ID */
  id?: number;
  /** Workout types */
  workout_types: Record<string, string | null>;
  /**
   * Entry date
   * @format date
   */
  entry_date: string;
  /**
   * Workout type
   * @minLength 1
   * @maxLength 50
   */
  workout_type: string;
  /**
   * Activity type
   * @minLength 1
   * @maxLength 50
   */
  activity_type: string;
  /**
   * Scheduled dow
   * @min -2147483648
   * @max 2147483647
   */
  scheduled_dow: number;
  /** Scheduled length */
  scheduled_length: number;
  /** Scheduled length2 */
  scheduled_length2: number;
  /** Actual length */
  actual_length: number;
  /**
   * Notes
   * @minLength 1
   * @maxLength 2000
   */
  notes: string;
  season?: {
    /** ID */
    id?: number;
    /** Training plan */
    training_plan: 'CTB' | 'TCC';
    /**
     * Season start date
     * @format date
     */
    season_start_date: string;
    /**
     * Season end date
     * @format date
     */
    season_end_date: string;
    /** Params */
    params: object;
    user?: {
      /** ID */
      id?: number;
      /**
       * Password
       * @minLength 1
       * @maxLength 128
       */
      password: string;
      /**
       * Last login
       * @format date-time
       */
      last_login?: string | null;
      /**
       * Superuser status
       * Designates that this user has all permissions without explicitly assigning them.
       */
      is_superuser?: boolean;
      /**
       * Username
       * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
       * @minLength 1
       * @maxLength 150
       * @pattern ^[\w.@+-]+$
       */
      username: string;
      /**
       * First name
       * @maxLength 150
       */
      first_name?: string;
      /**
       * Last name
       * @maxLength 150
       */
      last_name?: string;
      /**
       * Email address
       * @format email
       * @maxLength 254
       */
      email?: string;
      /**
       * Staff status
       * Designates whether the user can log into this admin site.
       */
      is_staff?: boolean;
      /**
       * Active
       * Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
       */
      is_active?: boolean;
      /**
       * Date joined
       * @format date-time
       */
      date_joined?: string;
      /**
       * The groups this user belongs to. A user will get all permissions granted to each of their groups.
       * @uniqueItems true
       */
      groups?: number[];
      /**
       * Specific permissions for this user.
       * @uniqueItems true
       */
      user_permissions?: number[];
    };
  };
  week?: {
    /** ID */
    id?: number;
    /**
     * Week start date
     * @format date
     */
    week_start_date: string;
    /**
     * Week type
     * @minLength 1
     * @maxLength 50
     */
    week_type: string;
    /**
     * Week type num
     * @min -2147483648
     * @max 2147483647
     */
    week_type_num: number;
    season?: {
      /** ID */
      id?: number;
      /** Training plan */
      training_plan: 'CTB' | 'TCC';
      /**
       * Season start date
       * @format date
       */
      season_start_date: string;
      /**
       * Season end date
       * @format date
       */
      season_end_date: string;
      /** Params */
      params: object;
      /** User */
      user: number;
    };
  };
}

export interface TrainingBiblePreviewOut {
  entries: TrainingEntryOut[];
  hour_selection: number[];
}

export interface User {
  /** ID */
  id?: number;
  /**
   * Last login
   * @format date-time
   */
  last_login?: string | null;
  /**
   * Username
   * Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
   * @minLength 1
   * @maxLength 150
   * @pattern ^[\w.@+-]+$
   */
  username: string;
  /**
   * First name
   * @maxLength 150
   */
  first_name?: string;
  /**
   * Last name
   * @maxLength 150
   */
  last_name?: string;
  /**
   * Email address
   * @format email
   * @maxLength 254
   */
  email?: string;
  /**
   * Active
   * Designates whether this user should be treated as active. Unselect this instead of deleting accounts.
   */
  is_active?: boolean;
  /**
   * Date joined
   * @format date-time
   */
  date_joined?: string;
}

export interface LoginUser {
  /**
   * Username
   * @minLength 1
   */
  username: string;
  /**
   * Password
   * @minLength 1
   */
  password: string;
}

export interface SignupUser {
  /**
   * Username
   * @minLength 1
   */
  username: string;
  /**
   * Password
   * @minLength 1
   */
  password: string;
  /**
   * Password2
   * @minLength 1
   */
  password2: string;
}

export type StravaCallBack = object;

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, 'body' | 'bodyUsed'>;

export interface FullRequestParams extends Omit<RequestInit, 'body'> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<FullRequestParams, 'body' | 'method' | 'query' | 'path'>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, 'baseUrl' | 'cancelToken' | 'signal'>;
  securityWorker?: (securityData: SecurityDataType | null) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown> extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = 'application/json',
  FormData = 'multipart/form-data',
  UrlEncoded = 'application/x-www-form-urlencoded',
  Text = 'text/plain',
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = 'http://localhost:3000/api';
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>['securityWorker'];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) => fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: 'same-origin',
    headers: {},
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === 'number' ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join('&');
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter(key => 'undefined' !== typeof query[key]);
    return keys.map(key => (Array.isArray(query[key]) ? this.addArrayQueryParam(query, key) : this.addQueryParam(query, key))).join('&');
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : '';
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === 'object' || typeof input === 'string') ? JSON.stringify(input) : input,
    [ContentType.Text]: (input: any) => (input !== null && typeof input !== 'string' ? JSON.stringify(input) : input),
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === 'object' && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(params1: RequestParams, params2?: RequestParams): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (cancelToken: CancelToken): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === 'boolean' ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(`${baseUrl || this.baseUrl || ''}${path}${queryString ? `?${queryString}` : ''}`, {
      ...requestParams,
      headers: {
        ...(requestParams.headers || {}),
        ...(type && type !== ContentType.FormData ? { 'Content-Type': type } : {}),
      },
      signal: (cancelToken ? this.createAbortSignal(cancelToken) : requestParams.signal) || null,
      body: typeof body === 'undefined' || body === null ? null : payloadFormatter(body),
    }).then(async response => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then(data => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch(e => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title Bikes API
 * @version v1
 * @baseUrl http://localhost:3000/api
 */
export class Api<SecurityDataType extends unknown> extends HttpClient<SecurityDataType> {
  activities = {
    /**
     * No description
     *
     * @tags activities
     * @name ActivitiesList
     * @request GET:/activities/
     * @secure
     */
    activitiesList: (
      query?: {
        /** type */
        type?: string;
        /** trainer */
        trainer?: string;
        /** commute */
        commute?: string;
        /** manual */
        manual?: string;
        /** private */
        private?: string;
        /** flagged */
        flagged?: string;
        /** start_datetime */
        start_datetime?: string;
        /** start_datetime__gt */
        start_datetime__gt?: string;
        /** start_datetime__lt */
        start_datetime__lt?: string;
        /** start_datetime__gte */
        start_datetime__gte?: string;
        /** start_datetime__lte */
        start_datetime__lte?: string;
        /** start_datetime_local */
        start_datetime_local?: string;
        /** start_datetime_local__gt */
        start_datetime_local__gt?: string;
        /** start_datetime_local__lt */
        start_datetime_local__lt?: string;
        /** start_datetime_local__gte */
        start_datetime_local__gte?: string;
        /** start_datetime_local__lte */
        start_datetime_local__lte?: string;
        /** moving_time */
        moving_time?: string;
        /** moving_time__gt */
        moving_time__gt?: string;
        /** moving_time__lt */
        moving_time__lt?: string;
        /** moving_time__gte */
        moving_time__gte?: string;
        /** moving_time__lte */
        moving_time__lte?: string;
        /** elapsed_time */
        elapsed_time?: string;
        /** elapsed_time__gt */
        elapsed_time__gt?: string;
        /** elapsed_time__lt */
        elapsed_time__lt?: string;
        /** elapsed_time__gte */
        elapsed_time__gte?: string;
        /** elapsed_time__lte */
        elapsed_time__lte?: string;
        /** total_elevation_gain */
        total_elevation_gain?: string;
        /** total_elevation_gain__gt */
        total_elevation_gain__gt?: string;
        /** total_elevation_gain__lt */
        total_elevation_gain__lt?: string;
        /** total_elevation_gain__gte */
        total_elevation_gain__gte?: string;
        /** total_elevation_gain__lte */
        total_elevation_gain__lte?: string;
        /** achievement_count */
        achievement_count?: string;
        /** achievement_count__gt */
        achievement_count__gt?: string;
        /** achievement_count__lt */
        achievement_count__lt?: string;
        /** achievement_count__gte */
        achievement_count__gte?: string;
        /** achievement_count__lte */
        achievement_count__lte?: string;
        /** average_speed */
        average_speed?: string;
        /** average_speed__gt */
        average_speed__gt?: string;
        /** average_speed__lt */
        average_speed__lt?: string;
        /** average_speed__gte */
        average_speed__gte?: string;
        /** average_speed__lte */
        average_speed__lte?: string;
        /** max_speed */
        max_speed?: string;
        /** max_speed__gt */
        max_speed__gt?: string;
        /** max_speed__lt */
        max_speed__lt?: string;
        /** max_speed__gte */
        max_speed__gte?: string;
        /** max_speed__lte */
        max_speed__lte?: string;
        /** average_watts */
        average_watts?: string;
        /** average_watts__gt */
        average_watts__gt?: string;
        /** average_watts__lt */
        average_watts__lt?: string;
        /** average_watts__gte */
        average_watts__gte?: string;
        /** average_watts__lte */
        average_watts__lte?: string;
        /** max_watts */
        max_watts?: string;
        /** max_watts__gt */
        max_watts__gt?: string;
        /** max_watts__lt */
        max_watts__lt?: string;
        /** max_watts__gte */
        max_watts__gte?: string;
        /** max_watts__lte */
        max_watts__lte?: string;
        /** weighted_average_watts */
        weighted_average_watts?: string;
        /** weighted_average_watts__gt */
        weighted_average_watts__gt?: string;
        /** weighted_average_watts__lt */
        weighted_average_watts__lt?: string;
        /** weighted_average_watts__gte */
        weighted_average_watts__gte?: string;
        /** weighted_average_watts__lte */
        weighted_average_watts__lte?: string;
        /** kilojoules */
        kilojoules?: string;
        /** kilojoules__gt */
        kilojoules__gt?: string;
        /** kilojoules__lt */
        kilojoules__lt?: string;
        /** kilojoules__gte */
        kilojoules__gte?: string;
        /** kilojoules__lte */
        kilojoules__lte?: string;
        /** average_heartrate */
        average_heartrate?: string;
        /** average_heartrate__gt */
        average_heartrate__gt?: string;
        /** average_heartrate__lt */
        average_heartrate__lt?: string;
        /** average_heartrate__gte */
        average_heartrate__gte?: string;
        /** average_heartrate__lte */
        average_heartrate__lte?: string;
        /** max_heartrate */
        max_heartrate?: string;
        /** max_heartrate__gt */
        max_heartrate__gt?: string;
        /** max_heartrate__lt */
        max_heartrate__lt?: string;
        /** max_heartrate__gte */
        max_heartrate__gte?: string;
        /** max_heartrate__lte */
        max_heartrate__lte?: string;
        /** suffer_score */
        suffer_score?: string;
        /** suffer_score__gt */
        suffer_score__gt?: string;
        /** suffer_score__lt */
        suffer_score__lt?: string;
        /** suffer_score__gte */
        suffer_score__gte?: string;
        /** suffer_score__lte */
        suffer_score__lte?: string;
        /** A search term. */
        search?: string;
        /** Which field to use when ordering the results. */
        ordering?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count: number;
          /** @format uri */
          next?: string | null;
          /** @format uri */
          previous?: string | null;
          results: ActivityOut[];
        },
        any
      >({
        path: `/activities/`,
        method: 'GET',
        query: query,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags activities
     * @name ActivitiesRead
     * @request GET:/activities/{activity_id}/
     * @secure
     */
    activitiesRead: (activityId: number, params: RequestParams = {}) =>
      this.request<ActivityOut, any>({
        path: `/activities/${activityId}/`,
        method: 'GET',
        secure: true,
        format: 'json',
        ...params,
      }),
  };
  seasons = {
    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsList
     * @request GET:/seasons/
     * @secure
     */
    seasonsList: (
      query?: {
        /** A search term. */
        search?: string;
        /** Which field to use when ordering the results. */
        ordering?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count: number;
          /** @format uri */
          next?: string | null;
          /** @format uri */
          previous?: string | null;
          results: Season[];
        },
        any
      >({
        path: `/seasons/`,
        method: 'GET',
        query: query,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsCreate
     * @request POST:/seasons/
     * @secure
     */
    seasonsCreate: (data: Season, params: RequestParams = {}) =>
      this.request<Season, any>({
        path: `/seasons/`,
        method: 'POST',
        body: data,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsPreviewTrainingBibleV1
     * @request POST:/seasons/preview_training_bible_v1/
     * @secure
     */
    seasonsPreviewTrainingBibleV1: (data: TrainingBibleV1In, params: RequestParams = {}) =>
      this.request<TrainingBiblePreviewOut, any>({
        path: `/seasons/preview_training_bible_v1/`,
        method: 'POST',
        body: data,
        secure: true,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsRead
     * @request GET:/seasons/{id}/
     * @secure
     */
    seasonsRead: (id: number, params: RequestParams = {}) =>
      this.request<Season, any>({
        path: `/seasons/${id}/`,
        method: 'GET',
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsUpdate
     * @request PUT:/seasons/{id}/
     * @secure
     */
    seasonsUpdate: (id: number, data: Season, params: RequestParams = {}) =>
      this.request<Season, any>({
        path: `/seasons/${id}/`,
        method: 'PUT',
        body: data,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsPartialUpdate
     * @request PATCH:/seasons/{id}/
     * @secure
     */
    seasonsPartialUpdate: (id: number, data: Season, params: RequestParams = {}) =>
      this.request<Season, any>({
        path: `/seasons/${id}/`,
        method: 'PATCH',
        body: data,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags seasons
     * @name SeasonsDelete
     * @request DELETE:/seasons/{id}/
     * @secure
     */
    seasonsDelete: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/seasons/${id}/`,
        method: 'DELETE',
        secure: true,
        ...params,
      }),
  };
  users = {
    /**
     * No description
     *
     * @tags users
     * @name UsersList
     * @request GET:/users/
     * @secure
     */
    usersList: (
      query?: {
        /** A search term. */
        search?: string;
        /** Which field to use when ordering the results. */
        ordering?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count: number;
          /** @format uri */
          next?: string | null;
          /** @format uri */
          previous?: string | null;
          results: User[];
        },
        any
      >({
        path: `/users/`,
        method: 'GET',
        query: query,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags users
     * @name UsersLogin
     * @request POST:/users/login/
     * @secure
     */
    usersLogin: (data: LoginUser, params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/users/login/`,
        method: 'POST',
        body: data,
        secure: true,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags users
     * @name UsersSignup
     * @request POST:/users/signup/
     * @secure
     */
    usersSignup: (data: SignupUser, params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/users/signup/`,
        method: 'POST',
        body: data,
        secure: true,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags users
     * @name UsersStravaCallback
     * @request POST:/users/strava_callback/
     * @secure
     */
    usersStravaCallback: (data: StravaCallBack, params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/users/strava_callback/`,
        method: 'POST',
        body: data,
        secure: true,
        type: ContentType.Json,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags users
     * @name UsersStravaConnect
     * @request GET:/users/strava_connect/
     * @secure
     */
    usersStravaConnect: (
      query?: {
        /** A search term. */
        search?: string;
        /** Which field to use when ordering the results. */
        ordering?: string;
        /** Number of results to return per page. */
        limit?: number;
        /** The initial index from which to return the results. */
        offset?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<
        {
          count: number;
          /** @format uri */
          next?: string | null;
          /** @format uri */
          previous?: string | null;
          results: User[];
        },
        any
      >({
        path: `/users/strava_connect/`,
        method: 'GET',
        query: query,
        secure: true,
        format: 'json',
        ...params,
      }),

    /**
     * No description
     *
     * @tags users
     * @name UsersRead
     * @request GET:/users/{id}/
     * @secure
     */
    usersRead: (id: number, params: RequestParams = {}) =>
      this.request<User, any>({
        path: `/users/${id}/`,
        method: 'GET',
        secure: true,
        format: 'json',
        ...params,
      }),
  };
}
