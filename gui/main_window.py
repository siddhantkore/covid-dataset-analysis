import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
		# Keep floating toggle at top-left edge when visible
		if not self.sidebar_expanded:
			try:
				self.floating_toggle.place_configure(relx=0.0, rely=0.09)
			except Exception:
				pass

	def _clear_content(self):
		for widget in self.content.winfo_children():
			widget.destroy()

	def _on_tab_change(self):
		tab = self.current_tab.get()
		if tab == "Dashboard":
			self._show_dashboard()
		elif tab == "Data":
			self._show_data()
		elif tab == "About Us":
			self._show_about()

	def _show_dashboard(self):
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
		self._clear_content()
		about = tk.Frame(self.content, bg=COLOR_PALETTE['bg'])
		about.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
		tk.Label(about, text="About Us", font=TITLE_FONT, bg=COLOR_PALETTE['bg'], fg=COLOR_PALETTE['text']).pack(anchor="w")
		tk.Label(about, text="COVID-19 Dataset Analyzer\nDeveloped by Siddhant Kore\n\nFor documentation and more info, see the README.",
				 font=APP_FONT, bg=COLOR_PALETTE['bg'], fg=COLOR_PALETTE['text'], justify="left").pack(anchor="w", pady=10)

	def _upload_file(self):
		file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
		if file_path:
			try:
				self.data = pd.read_csv(file_path)
				# self.data = cp.load_data_from_file(file_path)
				if self.data == FileNotFoundError:
					messagebox.showerror("Error", f"Failed to load file: {e}")
				# Extract dropdown options
				self.state_menu['values'] = sorted(self.data['Region'].unique())
				self.data['Month'] = pd.to_datetime(self.data['Date'], format='mixed').dt.month
				self.data['Year'] = pd.to_datetime(self.data['Date'], format='mixed').dt.year
				self.month_menu['values'] = sorted(self.data['Month'].unique()) if 'Month' in self.data else []
				self.year_menu['values'] = sorted(self.data['Year'].unique()) if 'Year' in self.data else []
				self.state_var.set(self.state_menu['values'][0] if self.state_menu['values'] else "")
				self.month_var.set(self.month_menu['values'][0] if self.month_menu['values'] else "")
				self.year_var.set(self.year_menu['values'][0] if self.year_menu['values'] else "")
				self._update_graph()
				messagebox.showinfo("Success", "Data loaded successfully!")
			except Exception as e:
				messagebox.showerror("Error", f"Failed to load file: {e}")

	def _update_graph(self):
		for widget in self.graph_frame.winfo_children():
			widget.destroy()
		if self.data is None or not all(col in self.data for col in ['Region', 'Month', 'Year', self.case_type_var.get()]):
			tk.Label(self.graph_frame, text="No data or missing columns.", font=APP_FONT, bg=COLOR_PALETTE['canvas_bg'], fg='red').pack(expand=True)
			return
		# Filter data
		df = self.data.copy()
		if self.state_var.get():
			df = df[df['Region'] == self.state_var.get()]
		if self.month_var.get():
			df = df[df['Month'] == int(self.month_var.get())]
		if self.year_var.get():
			df = df[df['Year'] == int(self.year_var.get())]
		if df.empty:
			tk.Label(self.graph_frame, text="No data for selected criteria.", font=APP_FONT, bg=COLOR_PALETTE['canvas_bg'], fg='red').pack(expand=True)
			return
		# Plot
		fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
		graph_type = self.graph_type_var.get().lower()
		x = 'Month' if self.month_var.get() else 'Year'
		y = self.case_type_var.get()
		if graph_type == 'line':
			ax.plot(df[x], df[y], marker='o', color=COLOR_PALETTE['accent'])
		elif graph_type == 'bar':
			ax.bar(df[x], df[y], color=COLOR_PALETTE['accent'])
		elif graph_type == 'scatter':
			ax.scatter(df[x], df[y], color=COLOR_PALETTE['accent'])
		ax.set_xlabel(x, fontname=APP_FONT[0])
		ax.set_ylabel(y, fontname=APP_FONT[0])
		ax.set_title(f"{y} by {x}", fontname=APP_FONT[0], fontsize=14)
		fig.tight_layout()
		canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
		canvas.draw()
		canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
		self.current_figure = fig

	def _download_graph(self):
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

