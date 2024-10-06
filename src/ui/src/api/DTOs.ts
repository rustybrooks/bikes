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

export interface TrainingWeekOut {
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
  /** Season */
  season?: number | null;
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
    activitiesList: (params: RequestParams = {}) =>
      this.request<ActivityOut[], any>({
        path: `/activities/`,
        method: 'GET',
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
    seasonsList: (params: RequestParams = {}) =>
      this.request<Season[], any>({
        path: `/seasons/`,
        method: 'GET',
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
      this.request<TrainingWeekOut[], any>({
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
    usersList: (params: RequestParams = {}) =>
      this.request<User[], any>({
        path: `/users/`,
        method: 'GET',
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
    usersStravaCallback: (data: User, params: RequestParams = {}) =>
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
    usersStravaConnect: (params: RequestParams = {}) =>
      this.request<User[], any>({
        path: `/users/strava_connect/`,
        method: 'GET',
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
