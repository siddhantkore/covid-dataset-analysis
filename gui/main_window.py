import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

# Make sure the project root is on sys.path so local packages (analysis, data, etc.) can be imported
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
	sys.path.insert(0, PROJECT_ROOT)

from analysis.trends import create_figure

# import data.cleaning_pipeline as cp

# Configurable color palette and font
COLOR_PALETTE = {
	'bg': '#f5f6fa',
	'sidebar': '#273c75',
	'sidebar_active': '#40739e',
	'accent': '#00a8ff',
	'canvas_bg': '#ffffff',
	'text': '#353b48',
}
APP_FONT = ("Segoe UI", 11)
TITLE_FONT = ("Segoe UI", 16, "bold")


class MainWindow(tk.Tk):
	"""Main application window for the COVID-19 Dataset Analyzer.

	This class builds the main layout: a top heading bar, a left toggleable
	sidebar, a right controls sidebar, and the main content area which hosts
	the dashboard graph and data table. It is intentionally GUI-only; plotting
	logic is delegated to `analysis.trends.create_figure`.

	Attributes
	----------
	data : pandas.DataFrame | None
		Currently loaded dataset (None until a CSV is uploaded).
	current_tab : tkinter.StringVar
		Tracks the current selected tab (Dashboard/Data/About Us).
	... (other UI state variables)

	"""
	def __init__(self):
		super().__init__()
		self.title("COVID-19 Dataset Analyzer")
		self.geometry("1200x750")
		self.minsize(950, 650)
		self.configure(bg=COLOR_PALETTE['bg'])

		self.data = None
		self.current_tab = tk.StringVar(value="Dashboard")
		self.state_var = tk.StringVar()
		self.month_var = tk.StringVar()
		self.year_var = tk.StringVar()
		self.case_type_var = tk.StringVar(value="Confirmed Cases")
		self.graph_type_var = tk.StringVar(value="Line")
		self.sidebar_expanded = True

		self._build_layout()
		self._show_dashboard()

	def _build_layout(self):
		"""Construct all UI elements and layout frames.

		Creates the heading bar, left sidebar (with toggle), floating toggle
		handle, right controls sidebar, and main content frame. This method
		does not populate dynamic data; that occurs when a CSV is uploaded.

		Returns
		-------
		None
		"""
		# Top heading bar
		heading = tk.Frame(self, bg=COLOR_PALETTE['accent'], height=60)
		heading.pack(side=tk.TOP, fill=tk.X)
		heading.pack_propagate(False)
		tk.Label(heading, text="Covid-19 Data Analysis", font=TITLE_FONT, bg=COLOR_PALETTE['accent'], fg='white').pack(side=tk.LEFT, padx=30, pady=10)

		# Left sidebar (toggleable)
		self.sidebar = tk.Frame(self, bg=COLOR_PALETTE['sidebar'], width=180)
		self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
		self.sidebar.pack_propagate(False)

		toggle_btn = tk.Button(self.sidebar, text="☰", font=("Segoe UI", 16), bg=COLOR_PALETTE['sidebar'], fg='white', bd=0, activebackground=COLOR_PALETTE['sidebar_active'], command=self._toggle_sidebar)
		toggle_btn.pack(anchor="nw", padx=8, pady=8)

		self.sidebar_btns = []
		for tab in ["Dashboard", "Data", "About Us"]:
			btn = tk.Radiobutton(
				self.sidebar, text=tab, variable=self.current_tab, value=tab,
				indicatoron=False, width=18, pady=15, font=APP_FONT,
				bg=COLOR_PALETTE['sidebar'], fg='white', selectcolor=COLOR_PALETTE['sidebar_active'],
				activebackground=COLOR_PALETTE['sidebar_active'], activeforeground='white',
				command=self._on_tab_change
			)
			btn.pack(fill=tk.X, pady=2)
			self.sidebar_btns.append(btn)

		# Floating toggle (always present but hidden when sidebar is visible)
		self.floating_toggle = tk.Button(self, text="☰", font=("Segoe UI", 12), bg=COLOR_PALETTE['accent'], fg='white', bd=0, command=self._toggle_sidebar)
		# Use relative placement so it stays visible on resize and above other widgets
		self.floating_toggle.place(relx=0.0, rely=0.09, anchor='w')
		self.floating_toggle.lift()
		# Start visible only if sidebar is collapsed
		if self.sidebar_expanded:
			self.floating_toggle.place_forget()

		# Reposition floating toggle on resize to ensure visibility
		self.bind('<Configure>', self._on_window_configure)

		# Keyboard shortcut to toggle sidebar
		self.bind_all('<Control-b>', lambda e: self._toggle_sidebar())

		# Right sidebar for controls
		self.rightbar = tk.Frame(self, bg=COLOR_PALETTE['sidebar'], width=250)
		self.rightbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.rightbar.pack_propagate(False)

		# Upload section
		upload_label = tk.Label(self.rightbar, text="Upload Data", font=APP_FONT, bg=COLOR_PALETTE['sidebar'], fg='white')
		upload_label.pack(pady=(20, 5))
		upload_btn = tk.Button(self.rightbar, text="Upload CSV", font=APP_FONT, bg=COLOR_PALETTE['accent'], fg='white', command=self._upload_file)
		upload_btn.pack(pady=(0, 20))

		# Filter controls
		filter_label = tk.Label(self.rightbar, text="Visualization Options", font=APP_FONT, bg=COLOR_PALETTE['sidebar'], fg='white')
		filter_label.pack(pady=(10, 5))

		self._add_rightbar_option("State:", self.state_var, 'state_menu')
		self._add_rightbar_option("Month:", self.month_var, 'month_menu')
		self._add_rightbar_option("Year:", self.year_var, 'year_menu')
		self._add_rightbar_option("Case Type:", self.case_type_var, 'case_type_menu', ["Confirmed Cases", "Active Cases", "Cured/Discharged", "Death"])
		self._add_rightbar_option("Graph Type:", self.graph_type_var, 'graph_type_menu', ["Line", "Bar", "Scatter"])

		download_btn = tk.Button(self.rightbar, text="Download Graph", font=APP_FONT, bg=COLOR_PALETTE['accent'], fg='white', command=self._download_graph)
		download_btn.pack(pady=(20, 0))

		# Main content area
		self.content = tk.Frame(self, bg=COLOR_PALETTE['bg'])
		self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.content.grid_rowconfigure(1, weight=1)
		self.content.grid_columnconfigure(0, weight=1)

	def _add_rightbar_option(self, label, var, menu_attr, values=None):
		"""Add a labeled Combobox to the right controls sidebar.

		Parameters
		----------
		label : str
			Label text displayed to the left of the combobox.
		var : tkinter.Variable
			Variable bound to the combobox selection.
		menu_attr : str
			Attribute name to assign the created Combobox to (e.g. 'state_menu').
		values : list[str] | None
			Optional list of values to populate the Combobox. If None, an empty
			combobox is created and values should be set later when data is loaded.

		Returns
		-------
		None
		"""
		frame = tk.Frame(self.rightbar, bg=COLOR_PALETTE['sidebar'])
		frame.pack(fill=tk.X, padx=10, pady=2)
		tk.Label(frame, text=label, font=APP_FONT, bg=COLOR_PALETTE['sidebar'], fg='white').pack(side=tk.LEFT)
		if values is None:
			menu = ttk.Combobox(frame, textvariable=var, font=APP_FONT, width=14, state="readonly")
		else:
			menu = ttk.Combobox(frame, textvariable=var, font=APP_FONT, width=14, state="readonly", values=values)
		menu.pack(side=tk.RIGHT, padx=5)
		setattr(self, menu_attr, menu)

	def _toggle_sidebar(self):
		"""Toggle the visibility of the left sidebar.

		When collapsing the sidebar a floating toggle button is shown on the
		left edge so the user can reopen the sidebar. When expanding the
		sidebar the floating handle is hidden.

		This method updates ``self.sidebar_expanded`` accordingly.

		Returns
		-------
		None
		"""
		if self.sidebar_expanded:
			# hide the sidebar and show floating toggle
			self.sidebar.pack_forget()
			self.sidebar_expanded = False
			# ensure floating toggle is placed and visible
			self.floating_toggle.place(relx=0.0, rely=0.09, anchor='w')
			self.floating_toggle.lift()
		else:
			# restore sidebar and hide floating toggle
			# pack the sidebar before the main content so it stays on the left
			try:
				self.sidebar.pack(side=tk.LEFT, fill=tk.Y, before=self.content)
			except Exception:
				# fallback if 'before' fails in some Tk versions
				self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
			self.sidebar_expanded = True
			self.floating_toggle.place_forget()

	def _on_window_configure(self, event):
		"""Handle window resize/configure events.

		This ensures the floating toggle stays positioned correctly when the
		window is resized.

		Parameters
		----------
		event : tkinter.Event
			The configure event object (passed from Tk).

		Returns
		-------
		None
		"""
		# Keep floating toggle at top-left edge when visible
		if not self.sidebar_expanded:
			try:
				self.floating_toggle.place_configure(relx=0.0, rely=0.09)
			except Exception:
				pass

	def _clear_content(self):
		"""Remove all widgets from the main content frame.

		Used when switching tabs to destroy previous tab widgets and free
		space for the new content.

		Returns
		-------
		None
		"""
		for widget in self.content.winfo_children():
			widget.destroy()

	def _on_tab_change(self):
		"""Callback when the selected sidebar tab changes.

		Reads ``self.current_tab`` and displays the corresponding content
		by calling ``_show_dashboard``, ``_show_data`` or ``_show_about``.

		Returns
		-------
		None
		"""
		tab = self.current_tab.get()
		if tab == "Dashboard":
			self._show_dashboard()
		elif tab == "Data":
			self._show_data()
		elif tab == "About Us":
			self._show_about()

	def _show_dashboard(self):
		"""Build and display the dashboard view (graph canvas).

		The dashboard contains a frame where the current figure (created by
		``analysis.trends.create_figure``) is embedded. Dropdowns on the right
		sidebar are bound to update the graph automatically.

		Returns
		-------
		None
		"""
		self._clear_content()
		# Canvas for graph
		self.graph_frame = tk.Frame(self.content, bg=COLOR_PALETTE['canvas_bg'], bd=2, relief=tk.RIDGE)
		self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
		self.content.grid_rowconfigure(0, weight=1)
		self.content.grid_columnconfigure(0, weight=1)

		# Bind dropdowns to update graph
		for var in [self.state_var, self.month_var, self.year_var, self.case_type_var, self.graph_type_var]:
			var.trace_add('write', lambda *args: self._update_graph())

	def _show_data(self):
		"""Show the raw data in a table view.

		If no data is loaded a message is displayed. For a loaded DataFrame a
		``ttk.Treeview`` is populated with rows from ``self.data``.

		Returns
		-------
		None
		"""
		self._clear_content()
		tk.Label(self.content, text="Data Table", font=TITLE_FONT, bg=COLOR_PALETTE['bg'], fg=COLOR_PALETTE['text']).pack(anchor="w", padx=20, pady=(20, 5))
		if self.data is not None:
			table_frame = tk.Frame(self.content, bg=COLOR_PALETTE['bg'])
			table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
			cols = list(self.data.columns)
			tree = ttk.Treeview(table_frame, columns=cols, show='headings')
			for col in cols:
				tree.heading(col, text=col)
				tree.column(col, width=100, anchor='center')
			for _, row in self.data.iterrows():
				tree.insert('', 'end', values=list(row))
			tree.pack(fill=tk.BOTH, expand=True)
		else:
			tk.Label(self.content, text="No data loaded.", font=APP_FONT, bg=COLOR_PALETTE['bg'], fg='red').pack(pady=30)

	def _show_about(self):
		"""Display the About view with project/author information.

		Returns
		-------
		None
		"""
		self._clear_content()
		about = tk.Frame(self.content, bg=COLOR_PALETTE['bg'])
		about.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
		tk.Label(about, text="About Us", font=TITLE_FONT, bg=COLOR_PALETTE['bg'], fg=COLOR_PALETTE['text']).pack(anchor="w")
		tk.Label(about, text="COVID-19 Dataset Analyzer\nDeveloped by Siddhant Kore\n\nFor documentation and more info, see the README.",
				 font=APP_FONT, bg=COLOR_PALETTE['bg'], fg=COLOR_PALETTE['text'], justify="left").pack(anchor="w", pady=10)

	def _upload_file(self):
		"""Prompt the user to select a CSV file and load it into ``self.data``.

		This method:

		- Opens a file dialog filtered to CSV files.
		- Loads the CSV into a pandas DataFrame and stores it in ``self.data``.
		- Derives ``Month`` and ``Year`` columns from the parsed ``Date`` column.
		- Populates the right sidebar comboboxes with available options.

		Errors during loading are presented to the user via a messagebox.

		Returns
		-------
		None
		"""
		file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
		if file_path:
			try:
				# Load CSV into DataFrame
				self.data = pd.read_csv(file_path)
				# Basic validation: ensure required columns exist
				required = {'Date', 'Region'}
				missing = required - set(self.data.columns)
				if missing:
					messagebox.showerror("Error", f"CSV missing required columns: {', '.join(missing)}")
					return
				# Parse dates safely and create Year/Month columns
				self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')
				if self.data['Date'].isna().all():
					messagebox.showerror("Error", "Failed to parse any dates from the 'Date' column.")
					return
				self.data['Month'] = self.data['Date'].dt.month
				self.data['Year'] = self.data['Date'].dt.year
				# Populate combobox options (guard against missing columns)
				self.state_menu['values'] = sorted(self.data['Region'].dropna().unique())
				# Normalize combobox values to strings to avoid float-like values (e.g. '1.0')
				months = sorted(self.data['Month'].dropna().unique())
				years = sorted(self.data['Year'].dropna().unique())
				self.month_menu['values'] = [str(int(m)) for m in months]
				self.year_menu['values'] = [str(int(y)) for y in years]
				# Set defaults if possible
				if len(self.state_menu['values']):
					self.state_var.set(self.state_menu['values'][0])
				if len(self.month_menu['values']):
					self.month_var.set(self.month_menu['values'][0])
				if len(self.year_menu['values']):
					self.year_var.set(self.year_menu['values'][0])
				# Update graph
				self._update_graph()
				messagebox.showinfo("Success", "Data loaded successfully!")
			except Exception as e:
				messagebox.showerror("Error", f"Failed to load file: {e}")

	def _update_graph(self):
		"""Generate and embed a matplotlib Figure for the current selection.

		This method reads selection values (state/month/year/case/graph type),
		calls ``analysis.trends.create_figure`` and embeds the returned Figure
		inside the dashboard canvas. Errors are shown inline in the canvas.

		Returns
		-------
		None
		"""
		for widget in self.graph_frame.winfo_children():
			widget.destroy()
		if self.data is None:
			# No data loaded yet
			tk.Label(self.graph_frame, text="No data loaded.", font=APP_FONT, bg=COLOR_PALETTE['canvas_bg'], fg='red').pack(expand=True)
			return
		# Prepare plotting parameters
		state = self.state_var.get() or None
		# Parse month/year robustly (handle values like '1.0')
		month = None
		if self.month_var.get():
			try:
				month = int(float(self.month_var.get()))
			except Exception:
				month = None
		year = None
		if self.year_var.get():
			try:
				year = int(float(self.year_var.get()))
			except Exception:
				year = None
		case_type = self.case_type_var.get()
		graph_type = self.graph_type_var.get()
		try:
			fig = create_figure(self.data, state=state, month=month, year=year, case_type=case_type, graph_type=graph_type, palette=COLOR_PALETTE)
		except Exception as e:
			tk.Label(self.graph_frame, text=f"Error: {e}", font=APP_FONT, bg=COLOR_PALETTE['canvas_bg'], fg='red').pack(expand=True)
			return
		canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
		canvas.draw()
		canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
		self.current_figure = fig

	def _download_graph(self):
		"""Save the current figure to disk (PNG or PDF).

		Opens a save dialog and uses ``Figure.savefig`` to write the selected
		format. If no current figure is available a warning is shown.

		Returns
		-------
		None
		"""
		if not hasattr(self, 'current_figure') or self.current_figure is None:
			messagebox.showwarning("No Graph", "No graph to download.")
			return
		filetypes = [("PNG Image", "*.png"), ("PDF Document", "*.pdf")]
		file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=filetypes)
		if file_path:
			try:
				if file_path.endswith('.pdf'):
					self.current_figure.savefig(file_path, format='pdf')
				else:
					self.current_figure.savefig(file_path, format='png')
				messagebox.showinfo("Saved", f"Graph saved to {file_path}")
			except Exception as e:
				messagebox.showerror("Error", f"Failed to save graph: {e}")

if __name__ == "__main__":
	app = MainWindow()
	app.mainloop()

