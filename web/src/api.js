import axios from 'axios';

const TOKEN_KEY = 'auth_token';

// 1. If running locally (localhost), point to Django on port 8000.
// 2. If running on render (production), point to render.
const IS_LOCALHOST = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";

const API_URL = IS_LOCALHOST 
  ? "http://127.0.0.1:8000" 
  : "https://chem-flow-backend.onrender.com"; 


export function getToken() {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) {
    sessionStorage.setItem(TOKEN_KEY, token);
  } else {
    sessionStorage.removeItem(TOKEN_KEY);
  }
}


export const api = axios.create({
  baseURL: API_URL + '/api', 
});

api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export async function login(username, password) {
 
  const resp = await api.post('/auth/token/', { username, password });
  return resp.data;
}

export async function uploadDataset(file) {
  const form = new FormData();
  form.append('file', file);
  const resp = await api.post('/datasets/upload/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return resp.data;
}

export async function fetchHistory() {
  const resp = await api.get('/datasets/history/');
  return resp.data;
}

export async function fetchDataset(id) {
  const resp = await api.get(`/datasets/${id}/`);
  return resp.data;
}

export async function downloadReport(id) {
  const resp = await api.get(`/datasets/${id}/report/`, { responseType: 'blob' });
  return resp.data;
}