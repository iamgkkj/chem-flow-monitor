from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class Dataset:
    id: int
    created_at: str
    original_filename: str
    csv_file: str
    total_count: int
    avg_flowrate: Optional[float]
    avg_pressure: Optional[float]
    avg_temperature: Optional[float]
    type_distribution: Dict[str, int]


class ApiError(RuntimeError):
    pass


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None

    def _headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers

    def login(self, username: str, password: str) -> str:
        url = f'{self.base_url}/api/auth/token/'
        resp = requests.post(url, json={'username': username, 'password': password}, timeout=20)
        if resp.status_code != 200:
            raise ApiError(self._extract_error(resp))
        token = resp.json().get('token')
        if not token:
            raise ApiError('No token returned by server')
        self.token = token
        return token

    def upload_csv(self, file_path: str) -> Dataset:
        url = f'{self.base_url}/api/datasets/upload/'
        with open(file_path, 'rb') as f:
            resp = requests.post(
                url,
                headers=self._headers(),
                files={'file': (file_path.split('/')[-1], f, 'text/csv')},
                timeout=60,
            )
        if resp.status_code != 201:
            raise ApiError(self._extract_error(resp))
        return self._parse_dataset(resp.json())

    def history(self) -> List[Dataset]:
        url = f'{self.base_url}/api/datasets/history/'
        resp = requests.get(url, headers=self._headers(), timeout=20)
        if resp.status_code != 200:
            raise ApiError(self._extract_error(resp))
        return [self._parse_dataset(x) for x in resp.json()]

    def dataset_detail(self, dataset_id: int) -> Dataset:
        url = f'{self.base_url}/api/datasets/{dataset_id}/'
        resp = requests.get(url, headers=self._headers(), timeout=20)
        if resp.status_code != 200:
            raise ApiError(self._extract_error(resp))
        return self._parse_dataset(resp.json())

    def download_report_pdf(self, dataset_id: int) -> bytes:
        url = f'{self.base_url}/api/datasets/{dataset_id}/report/'
        resp = requests.get(url, headers=self._headers(), timeout=30)
        if resp.status_code != 200:
            raise ApiError(self._extract_error(resp))
        return resp.content

    def _parse_dataset(self, data: Dict[str, Any]) -> Dataset:
        return Dataset(
            id=int(data['id']),
            created_at=str(data.get('created_at', '')),
            original_filename=str(data.get('original_filename', '')),
            csv_file=str(data.get('csv_file', '')),
            total_count=int(data.get('total_count', 0)),
            avg_flowrate=data.get('avg_flowrate', None),
            avg_pressure=data.get('avg_pressure', None),
            avg_temperature=data.get('avg_temperature', None),
            type_distribution=dict(data.get('type_distribution', {}) or {}),
        )

    def _extract_error(self, resp: requests.Response) -> str:
        try:
            payload = resp.json()
            if isinstance(payload, dict):
                if 'detail' in payload:
                    return str(payload['detail'])
                return str(payload)
            return str(payload)
        except Exception:
            return f'HTTP {resp.status_code}: {resp.text}'
