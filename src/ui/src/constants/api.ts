const hostname = window && window.location.origin;

export const REMOTE_API = 'https://bikes.rustybrooks.com';
export const LOCAL_API = 'http://localhost:3000';

export const BASE_URL = hostname.includes('bikes') ? REMOTE_API : LOCAL_API;
