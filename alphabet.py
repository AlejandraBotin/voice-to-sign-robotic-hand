from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple, Union, Optional

import pandas as pd


FINGER_COLS = ["Thumb", "Index Finger", "Middle Finger", "Ring Finger", "Little Finger"]
WRIST_COL   = "Wrist"
CHAR_COL    = "Character"


@dataclass(frozen=True)
class AlphabetData:
    df: pd.DataFrame
    fingers: pd.DataFrame
    wrist: pd.Series
    mapping: Dict[str, Dict[str, Union[List[int], int]]]


def _read_table(path: Union[str, Path]) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    ext = path.suffix.lower()
    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if ext == ".csv":
        return pd.read_csv(path)

    raise ValueError(f"Formato no soportado: {ext}")


def load_alphabet(
    path: Union[str, Path],
    *,
    char_col: str = CHAR_COL,
    finger_cols: Optional[List[str]] = None,
    wrist_col: str = WRIST_COL,
    drop_empty_chars: bool = True,
) -> AlphabetData:
    finger_cols = finger_cols or FINGER_COLS

    df = _read_table(path)
    df.columns = [str(c).strip() for c in df.columns]

    required = [char_col] + finger_cols + [wrist_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Columnas no encontradas: {missing}. Disponibles: {list(df.columns)}")

    df = df[required].copy()
    df[char_col] = df[char_col].astype(str).str.strip()

    if drop_empty_chars:
        df = df[df[char_col].notna() & (df[char_col] != "")]

    for c in finger_cols + [wrist_col]:
        df[c] = pd.to_numeric(df[c], errors="raise").astype(int)

    mapping: Dict[str, Dict[str, Union[List[int], int]]] = {}
    for _, row in df.iterrows():
        ch = row[char_col]
        mapping[ch] = {
            "fingers": [int(row[c]) for c in finger_cols],
            "wrist": int(row[wrist_col]),
        }

    return AlphabetData(
        df=df,
        fingers=df[finger_cols].copy(),
        wrist=df[wrist_col].copy(),
        mapping=mapping,
    )


def get_pose(
    mapping: Dict[str, Dict[str, Union[List[int], int]]],
    character: str,
) -> Tuple[List[int], int]:
    character = character.strip()
    if character not in mapping:
        raise KeyError(f"Carácter '{character}' no encontrado en el alfabeto.")
    return list(mapping[character]["fingers"]), int(mapping[character]["wrist"])
