from __future__ import annotations

from typing import Any, Dict, Tuple

import pandas as pd

REQUIRED_COLUMNS = [
    'Equipment Name',
    'Type',
    'Flowrate',
    'Pressure',
    'Temperature',
]


def parse_equipment_csv(file_obj) -> Tuple[pd.DataFrame, str | None]:
    try:
        df = pd.read_csv(file_obj)
    except Exception as exc:
        return pd.DataFrame(), f'Invalid CSV: {exc}'

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return pd.DataFrame(), f"Missing required columns: {', '.join(missing)}"

    for col in ['Flowrate', 'Pressure', 'Temperature']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df, None


def compute_summary(df: pd.DataFrame) -> Dict[str, Any]:
    total_count = int(len(df.index))

    averages = {
        'avg_flowrate': float(df['Flowrate'].mean()) if total_count else None,
        'avg_pressure': float(df['Pressure'].mean()) if total_count else None,
        'avg_temperature': float(df['Temperature'].mean()) if total_count else None,
    }

    type_distribution = (
        df['Type']
        .fillna('')
        .astype(str)
        .replace({'': 'Unknown'})
        .value_counts()
        .to_dict()
    )

    return {
        'total_count': total_count,
        **averages,
        'type_distribution': type_distribution,
    }
