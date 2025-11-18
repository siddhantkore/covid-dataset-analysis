# from gui.welcome_page import WelcomePage
# from __init__ import open_main_page

# if __name__ == "__main__":
# 	app = WelcomePage(open_main_page)
# 	app.mainloop()


import tkinter as tk
from tkinter import ttk

# 🎨 Color Palette
COLORS = {
    "bg": "#F7FAFC",         # background
    "sidebar": "#E3F2FD",    # sidebar panel
    "primary": "#4FC3F7",    # primary button
    "primary_hover": "#29B6F6",
    "success": "#81C784",    # recovery
    "danger": "#E57373",     # deaths
    "neutral": "#90A4AE",    # neutral text
    "header": "#37474F",     # header text
    "status": "#C8E6C9",     # status bar
}


class CovidApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("COVID-19 Data Analysis")
        self.geometry("1200x700")
        self.configure(bg=COLORS["bg"])
        self.minsize(1000, 600)

        # Header / Top Bar
        self.create_header()

        # Layout Panels
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()

    def create_header(self):
        header_frame = tk.Frame(self, bg=COLORS["primary"], height=60)
        header_frame.pack(side="top", fill="x")

        # App Logo (placeholder text instead of icon for now)
        logo = tk.Label(
            header_frame,
            text="",
            bg=COLORS["primary"],
            fg="white",
            font=("Arial", 20, "bold"),
        )
        logo.pack(side="left", padx=10)

        # Title
        title = tk.Label(
            header_frame,
            text="COVID-19 Data Analysis",
            bg=COLORS["primary"],
            fg="white",
            font=("Arial", 18, "bold"),
        )
        title.pack(side="left", padx=5)

        # Optional Menu Bar
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Upload")
        file_menu.add_command(label="Save Chart")
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=250)
        sidebar.pack(side="left", fill="y")

        # Upload Section
        upload_label = tk.Label(
            sidebar,
            text="Upload Dataset 📂",
            bg=COLORS["sidebar"],
            fg=COLORS["header"],
            font=("Arial", 12, "bold"),
        )
        upload_label.pack(pady=(15, 5))

        upload_button = tk.Button(
            sidebar,
            text="Choose File",
            bg=COLORS["primary"],
            fg="white",
            relief="flat",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
        )
        upload_button.pack(pady=5)

        file_label = tk.Label(
            sidebar,
            text="No file selected",
            bg=COLORS["sidebar"],
            fg=COLORS["neutral"],
            font=("Arial", 10),
        )
        file_label.pack(pady=(0, 20))

        # Filters
        filter_label = tk.Label(
            sidebar,
            text="Filters 🌍",
            bg=COLORS["sidebar"],
            fg=COLORS["header"],
            font=("Arial", 12, "bold"),
        )
        filter_label.pack(pady=(10, 5))

        ttk.Combobox(sidebar, values=["Select Country/State"]).pack(pady=5, padx=10)
        ttk.Combobox(sidebar, values=["Daily Cases", "Weekly Cases", "Recovery vs Death", "Distribution"]).pack(pady=5, padx=10)

        # Date Range Selector (static placeholder)
        tk.Entry(sidebar).pack(pady=5, padx=10, fill="x")
        tk.Entry(sidebar).pack(pady=5, padx=10, fill="x")

        # Action Buttons
        tk.Button(sidebar, text="▶ Generate Chart", bg=COLORS["primary"], fg="white", relief="flat", padx=10, pady=5).pack(pady=(20, 5))
        tk.Button(sidebar, text="♻ Reset", bg=COLORS["neutral"], fg="white", relief="flat", padx=10, pady=5).pack(pady=5)
        tk.Button(sidebar, text="💾 Export Chart", bg=COLORS["success"], fg="white", relief="flat", padx=10, pady=5).pack(pady=5)

    def create_main_content(self):
        main_content = tk.Frame(self, bg=COLORS["bg"])
        main_content.pack(side="left", fill="both", expand=True)

        # Placeholder for Matplotlib Canvas
        chart_placeholder = tk.Label(
            main_content,
            text="(Chart Area)",
            bg=COLORS["bg"],
            fg=COLORS["neutral"],
            font=("Arial", 16, "italic"),
        )
        chart_placeholder.pack(expand=True)

        # Toolbar
        toolbar = tk.Frame(main_content, bg=COLORS["bg"])
        toolbar.pack(fill="x", pady=10)
        tk.Button(toolbar, text="🔍 +", bg=COLORS["primary"], fg="white", relief="flat").pack(side="left", padx=5)
        tk.Button(toolbar, text="🔍 -", bg=COLORS["primary"], fg="white", relief="flat").pack(side="left", padx=5)
        tk.Button(toolbar, text="⬅ Back", bg=COLORS["neutral"], fg="white", relief="flat").pack(side="left", padx=5)

    def create_status_bar(self):
        status_bar = tk.Label(
            self,
            text="Ready",
            bg=COLORS["status"],
            fg=COLORS["header"],
            anchor="w",
            font=("Arial", 10),
        )
        status_bar.pack(side="bottom", fill="x")


if __name__ == "__main__":
    app = CovidApp()
    app.mainloop()

