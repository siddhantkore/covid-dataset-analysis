
"""Chart-generation helpers for the COVID-19 dataset analyzer.

This module exposes a small API that takes a DataFrame and plotting options
and returns a matplotlib.figure.Figure object ready to be embedded in the GUI.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_figure(df: pd.DataFrame,
				  state: str = None,
				  month: int | None = None,
				  year: int | None = None,
				  case_type: str = "Confirmed Cases",
				  graph_type: str = "Line",
				  palette: dict | None = None) -> plt.Figure:
	"""Create and return a matplotlib Figure based on the provided options.

	Args:
		- df: Input DataFrame containing at least 'Date' and numeric case columns.
		- state: Optional region to filter by (value from 'Region' column).
		- month: Optional month (1-12) to filter by.
		- year: Optional year to filter by.
		- case_type: Column name to plot (e.g. 'Death').
		- graph_type: One of 'Line', 'Bar', 'Scatter'.
		- palette: Optional color palette dict; expects key 'accent' for line/bar color.

	Returns:
		- matplotlib.figure.Figure

	Raises:
		- ValueError: if no data after filtering or required columns missing.
	"""
	if palette is None:
		palette = {'accent': '#00a8ff'}

	# Ensure date parsing and Year/Month/Day columns exist
	if 'Date' in df.columns and not pd.api.types.is_datetime64_any_dtype(df['Date']):
		df = df.copy()
		df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
	if 'Month' not in df.columns and 'Date' in df.columns:
		df['Month'] = df['Date'].dt.month
	if 'Year' not in df.columns and 'Date' in df.columns:
		df['Year'] = df['Date'].dt.year
	if 'Day' not in df.columns and 'Date' in df.columns:
		df['Day'] = df['Date'].dt.day

	# Filter
	plot_df = df.copy()
	if state:
		if 'Region' not in plot_df.columns:
			raise ValueError("'Region' column not found in DataFrame")
		plot_df = plot_df[plot_df['Region'] == state]
	if month is not None:
		if 'Month' not in plot_df.columns:
			raise ValueError("'Month' column not found in DataFrame")
		plot_df = plot_df[plot_df['Month'] == int(month)]
	if year is not None:
		if 'Year' not in plot_df.columns:
			raise ValueError("'Year' column not found in DataFrame")
		plot_df = plot_df[plot_df['Year'] == int(year)]

	if plot_df.empty:
		raise ValueError("No data for selected criteria")

	# Decide x-axis column
	if month is not None and 'Day' in plot_df.columns:
		x_col = 'Day'
	elif year is not None and 'Month' in plot_df.columns:
		x_col = 'Month'
	else:
		x_col = 'Year' if 'Year' in plot_df.columns else 'Date'

	if case_type not in plot_df.columns:
		raise ValueError(f"Column '{case_type}' not found in DataFrame")

	fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
	color = palette.get('accent', '#00a8ff')
	gtype = graph_type.lower()
	if gtype == 'line':
		ax.plot(plot_df[x_col], plot_df[case_type], marker='o', color=color)
	elif gtype == 'bar':
		ax.bar(plot_df[x_col], plot_df[case_type], color=color)
	elif gtype == 'scatter':
		ax.scatter(plot_df[x_col], plot_df[case_type], color=color)
	else:
		raise ValueError(f"Unknown graph type: {graph_type}")

	ax.set_xlabel(x_col)
	ax.set_ylabel(case_type)
	ax.set_title(f"{case_type} by {x_col}")
	fig.tight_layout()
	return fig

