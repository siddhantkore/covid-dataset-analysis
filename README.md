<div align="center">

# 🦠 COVID-19 Dataset Analysis App

<img src="https://img.shields.io/badge/Python-3.8%2B-blue?logo=python" />
<img src="https://img.shields.io/badge/Tkinter-GUI-green" />
<img src="https://img.shields.io/badge/Pandas-Data%20Analysis-yellow?logo=pandas" />
<img src="https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=matplotlib" />
<img src="https://img.shields.io/badge/License-MIT-blue" />

<br>
<strong>A modern desktop app for COVID-19 data analysis and visualization</strong>
</div>

---

<div align="center">
<h3>📊 Analyze, Filter, and Visualize COVID-19 Data with Ease!</h3>
</div>

---

## 🚀 Features

- 📁 Upload CSV or Excel datasets
- 🌍 Filter by country/state
- 📈 Daily / Weekly Case Counts (Line Chart)
- 📊 Recovery vs Death Comparison (Stacked Bar Chart)
- 🥧 Case Distribution by State/Country (Pie Chart or Map)
- 🖼️ Interactive charts embedded in Tkinter window
- 🎨 Multiple visualization modes
- 🗂️ Example dataset included in `assets/sample_dataset.csv`

---

## 🛠️ Tech Stack

- **GUI:** Tkinter
- **Data Handling:** Pandas
- **Visualization:** Matplotlib, Seaborn
- **File Support:** CSV & Excel (openpyxl)
- **Optional Maps:** GeoPandas

---

## 📁 Project Structure

```text
covid_analysis_app/
│
├── main.py              # Entry point
├── gui/                 # Tkinter GUI components
├── data/                # Data loading & processing
├── analysis/            # Chart generation modules
├── utils/               # Helpers (validators, chart embedding)
├── assets/              # Sample dataset, icons
├── requirements.txt     # Dependencies
└── README.md            # Documentation
```

---

<div align="center">
<h3>🖥️ Screenshots</h3>
<em>(Add your screenshots here)</em>
</div>

---

## ⚡ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/covid-analysis-app.git
cd covid-analysis-app

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

---

## 📝 How to Use

1. **Upload** your dataset (CSV or Excel)
2. **Select** country/state from the dropdown
3. **Choose** analysis type:
	- Daily/Weekly Cases
	- Recovery vs Death
	- Case Distribution
4. Click **Generate** to view chart

---

## 📄 Dataset Format

Your dataset must have at least the following columns:

| date       | country | state       | cases | recoveries | deaths |
| ---------- | ------- | ----------- | ----- | ---------- | ------ |
| 2020-03-01 | India   | Kerala      | 5     | 0          | 0      |
| 2020-03-02 | India   | Kerala      | 10    | 1          | 0      |
| 2020-03-02 | India   | Maharashtra | 3     | 0          | 0      |

- **date**: YYYY-MM-DD format
- **cases**: new cases reported
- **recoveries**: number of recovered patients
- **deaths**: number of deaths

---

## 🌟 Future Enhancements

- Add more visualization types (heatmaps, histograms)
- Data export (filtered datasets, charts)
- Improved UI/UX and responsiveness
- Dark mode support
- Automated data updates from online sources

---

<div align="center">
<h3>👨‍💻 Developed by <a href="https://linkedin.com/in/siddhantkore0bb">Siddhant Kore</a></h3>
</div>