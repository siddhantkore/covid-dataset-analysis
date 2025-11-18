
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from calendar import monthrange

DEFAULT_CASE_COLUMNS = [
    "Confirmed Cases",
    "Active Cases",
    "Cured/Discharged",
    "Death",
]


def _ensure_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'Date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    if 'Year' not in df.columns and 'Date' in df.columns:
        df['Year'] = df['Date'].dt.year
    if 'Month' not in df.columns and 'Date' in df.columns:
        df['Month'] = df['Date'].dt.month
    if 'Day' not in df.columns and 'Date' in df.columns:
        df['Day'] = df['Date'].dt.day
    return df


def create_figure(df: pd.DataFrame,
                  state: str | None = None,
                  month: int | None = None,
                  year: int | None = None,
                  case_type: str = "Confirmed Cases",
                  graph_type: str = "Line",
                  palette: dict | None = None) -> plt.Figure:
    """
    Create a matplotlib Figure for different graph types.

    Supported graph_type values (case-insensitive):
      - line, bar, scatter, area, histogram, box, pie

    Behavior details:
      - When month is provided, X axis is integer days (1..N) and missing days are filled with 0.
      - When only year provided, X axis is months 1..12 (aggregated sum per month).
      - When neither provided, X axis is years (aggregated sum per year).
      - For pie charts: if state is None, pie shows sum of case_type per Region. If state provided, pie shows distribution across case columns for that state/selection.
    """
    if palette is None:
        palette = {'accent': '#00a8ff'}

    df = _ensure_date_columns(df)

    plot_df = df.copy()
    if state:
        plot_df = plot_df[plot_df['Region'] == state]
    if year is not None:
        plot_df = plot_df[plot_df['Year'] == int(year)]
    if month is not None:
        plot_df = plot_df[plot_df['Month'] == int(month)]

    if plot_df.empty:
        raise ValueError("No data for selected criteria")

    # Validate case_type
    if graph_type.lower() != 'pie' and case_type not in plot_df.columns:
        raise ValueError(f"Column '{case_type}' not found in DataFrame")

    fig, ax = plt.subplots(figsize=(9, 5), dpi=100)
    color = palette.get('accent', '#00a8ff')
    gtype = graph_type.lower()

    if gtype == 'pie':
        # two modes: per-region totals (state=None) OR distribution of case-types for selected subset
        if state is None:
            agg = plot_df.groupby('Region')[case_type].sum().sort_values(ascending=False)
            ax.pie(agg.values, labels=agg.index, autopct='%1.1f%%')
            ax.set_title(f"{case_type} distribution by Region")
        else:
            # for the selected subset, show breakdown across case columns
            totals = {c: int(plot_df[c].sum()) for c in DEFAULT_CASE_COLUMNS if c in plot_df.columns}
            labels = list(totals.keys())
            values = list(totals.values())
            if sum(values) == 0:
                raise ValueError("Selected subset sums to zero, cannot create pie chart")
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title(f"Case distribution for {state} ({'Month '+str(month) if month else ''}{' Year '+str(year) if year else ''})")
        fig.tight_layout()
        return fig

    # For other charts we determine x and y
    if month is not None:
        # ensure all days exist in the month
        # aggregate by day
        days_in_month = monthrange(int(year) if year is not None else int(plot_df['Year'].iloc[0]), int(month))[1]
        agg = plot_df.groupby('Day')[case_type].sum()
        
        full_index = pd.RangeIndex(1, days_in_month + 1)
        agg = agg.reindex(full_index, fill_value=0)
        x = list(agg.index)
        y = agg.values
        ax.set_xlabel('Day')
        ax.set_xticks(range(1, days_in_month + 1))
        ax.set_xticklabels([str(d) for d in range(1, days_in_month + 1)])
    elif year is not None:
        # aggregate by month 1..12
        agg = plot_df.groupby('Month')[case_type].sum()
        full_index = pd.RangeIndex(1, 13)
        agg = agg.reindex(full_index, fill_value=0)
        x = list(range(1, 13))
        y = agg.values
        ax.set_xlabel('Month')
        ax.set_xticks(x)
        ax.set_xticklabels([str(m) for m in x])
    else:
        # aggregate by year
        agg = plot_df.groupby('Year')[case_type].sum().sort_index()
        x = list(agg.index)
        y = agg.values
        ax.set_xlabel('Year')
        ax.set_xticks(x)
        ax.set_xticklabels([str(int(v)) for v in x])

    # Plot according to graph type
    if gtype == 'line':
        ax.plot(x, y, marker='o', color=color)
    elif gtype == 'bar':
        ax.bar(x, y, color=color)
    elif gtype == 'scatter':
        ax.scatter(x, y, color=color)
    elif gtype == 'area':
        ax.fill_between(x, y, step='mid', alpha=0.4)
        ax.plot(x, y, marker='o', color=color)
    elif gtype == 'histogram' or gtype == 'hist':
        # histogram of the raw selected case values
        raw = plot_df[case_type].dropna().values
        if raw.size == 0:
            raise ValueError("No numeric data available for histogram")
        ax.hist(raw)
        ax.set_xlabel(case_type)
        ax.set_ylabel('Frequency')
    elif gtype == 'box' or gtype == 'boxplot':
        raw = plot_df[case_type].dropna().values
        if raw.size == 0:
            raise ValueError("No numeric data available for boxplot")
        ax.boxplot(raw, vert=True)
        ax.set_ylabel(case_type)
    else:
        raise ValueError(f"Unknown graph type: {graph_type}")

    ax.set_ylabel(case_type)
    ax.set_title(f"{case_type} ({graph_type})")
    fig.tight_layout()
    return fig