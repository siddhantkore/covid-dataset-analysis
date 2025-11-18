
import pandas as pd
import numpy as np


DEFAULT_CASE_COLUMNS = [
    "Confirmed Cases",
    "Active Cases",
    "Cured/Discharged",
    "Death",
]


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Trim whitespace and normalize common column names to expected ones
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if lc in ("date", "dt"):
            col_map[c] = "Date"
        elif lc in ("region", "state", "state/ut"):
            col_map[c] = "Region"
        elif lc in ("confirmed cases", "confirmed", "cases"):
            col_map[c] = "Confirmed Cases"
        elif lc in ("active cases", "active"):
            col_map[c] = "Active Cases"
        elif lc in ("cured/discharged", "cured", "recovered", "discharged"):
            col_map[c] = "Cured/Discharged"
        elif lc in ("death", "deaths"):
            col_map[c] = "Death"
    df = df.rename(columns=col_map)
    return df


def load_data_from_file(path: str) -> pd.DataFrame:
    """
    Load CSV/XLSX and return cleaned DataFrame. Raises exceptions on failure.
    """
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path, dtype=str)
    elif path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(path, dtype=str)
    else:
        raise ValueError("Unsupported file type: expected .csv or .xlsx")

    df = _standardize_columns(df)
    return clean_data(df)


def clean_data(df: pd.DataFrame, min_year: int = 2020) -> pd.DataFrame:
    """
    Clean and normalize the DataFrame for plotting. Steps:
      - standardize column names
      - parse Date column to datetime (coerce invalid → NaT)
      - drop rows without Date or Region
      - enforce Year >= min_year (removes bad years like 1970, 2014, 2015)
      - convert case columns to numeric and fill NaN with 0
      - drop exact duplicates and reset index
    """
    if df is None:
        return pd.DataFrame()

    df = _standardize_columns(df)

    # Parse date
    df['Date'] = pd.to_datetime(df.get('Date'), dayfirst=True, errors='coerce')

    # Drop rows without valid date or region
    df['Region'] = df.get('Region').astype(str).str.strip()
    df = df.dropna(subset=['Date'])
    df = df[df['Region'].notna() & (df['Region'] != '')]

    # Year/Month/Day
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Remove obviously bad years (before min_year) unless user wants otherwise
    df = df[df['Year'] >= int(min_year)]

    # Ensure numeric columns exist and convert
    for col in DEFAULT_CASE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].str.replace('[^0-9\-\.]', '', regex=True), errors='coerce').fillna(0).astype(int)
        else:
            # add missing columns as zeros for consistency
            df[col] = 0

    # Remove duplicates (exact duplicate rows)
    df = df.drop_duplicates()

    # Sort by Date for predictable plotting
    df = df.sort_values('Date').reset_index(drop=True)

    return df


def remove_outliers(df: pd.DataFrame, case_columns: list | None = None, group_by: str = 'Year', iqr_multiplier: float = 1.5) -> pd.DataFrame:
    """
    Optional IQR-based outlier removal. Operates _in-place_ on a copy and returns cleaned df.
    Use this if you want to aggressively remove statistical outliers by group.
    """
    if case_columns is None:
        case_columns = DEFAULT_CASE_COLUMNS

    if df.empty:
        return df

    d = df.copy()
    for col in case_columns:
        if col not in d.columns:
            continue
        # compute IQR per group
        grouped = d.groupby(group_by)[col]
        q1 = grouped.transform(lambda s: s.quantile(0.25))
        q3 = grouped.transform(lambda s: s.quantile(0.75))
        iqr = q3 - q1
        lower = q1 - iqr_multiplier * iqr
        upper = q3 + iqr_multiplier * iqr
        mask = (d[col] >= lower) & (d[col] <= upper)
        d = d[mask]
    return d.reset_index(drop=True)
