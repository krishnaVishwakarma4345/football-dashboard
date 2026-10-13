# ⚽ Football Player Performance Analytics Dashboard

A portfolio-quality interactive analytics dashboard built with **Python** and **Streamlit**, designed to explore and compare football (soccer) player statistics.

> ⚠️ **Disclaimer:** All data displayed in this application is **fully synthetic and randomly generated**. It does not represent real football players, clubs, or match statistics from any league or competition.

---

## 📸 Features

| Page | What's Inside |
|---|---|
| **📊 Overview** | 5 live KPI cards · Top-10 player rating chart · Goals distribution histogram |
| **👤 Player Analysis** | Multi-player radar comparison · Goals vs Assists scatter · Shots vs Goals conversion chart |
| **🏟️ Team Analysis** | Team goals & assists grouped bar · Player count · Avg rating ranking |
| **🎽 Position Analysis** | Position stats bar chart · Rating box plot · Clean sheets (GK/DEF) |

**Plus on every page:**
- Searchable player statistics table
- ⬇️ CSV download of filtered data
- Sidebar filters: Season · Team · Position · Player name search

---

## 🛠️ Tech Stack

- [Python 3.9+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — web application framework
- [Pandas](https://pandas.pydata.org/) — data manipulation
- [NumPy](https://numpy.org/) — numerical generation
- [Plotly](https://plotly.com/python/) — interactive charts

---

## 📁 Project Structure

```
FOOTBALL/
├── app.py                  # Main Streamlit application (all pages)
├── football_players.csv    # Auto-generated synthetic dataset (423 rows)
├── generate_data.py        # Standalone dataset generator script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .streamlit/
    └── config.toml         # Dark theme configuration
```

---

## 🚀 Run Locally

### 1. Prerequisites

- Python **3.9 or higher** installed — check with `python --version`
- `pip` available — check with `pip --version`

### 2. Clone / Download the project

```bash
git clone https://github.com/your-username/football-analytics-dashboard.git
cd football-analytics-dashboard
```

Or download and unzip the project folder, then `cd` into it.

### 3. Create a virtual environment (recommended)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the app

```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`.

> **Note:** If `football_players.csv` does not exist, it is generated automatically on first launch with `numpy.random.seed(42)` — fully reproducible.

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

1. **Push the project to GitHub** — make sure `app.py`, `requirements.txt`, and `.streamlit/config.toml` are all committed.

2. **Sign in** at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.

3. Click **"New app"** and fill in:
   - **Repository:** `your-username/football-analytics-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`

4. Click **"Deploy"** — Streamlit Cloud installs dependencies and launches the app. You'll get a public shareable URL.

> The app automatically re-deploys whenever you push to the connected branch.

---

## 📊 Dataset Schema

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique player record ID |
| `player_name` | str | Realistic multi-cultural fictional name |
| `team` | str | One of 10 fictional club names |
| `position` | str | GK / DEF / MID / FWD |
| `season` | str | 2021-22 · 2022-23 · 2023-24 |
| `age` | int | Age 17–36 |
| `matches_played` | int | Appearances (1–38) |
| `minutes_played` | int | Total minutes |
| `goals` | int | Goals scored (position-weighted) |
| `assists` | int | Assists (position-weighted) |
| `shots` | int | Total shots attempted |
| `shots_on_target` | int | Shots on target |
| `passes` | int | Total passes |
| `pass_accuracy` | float | Pass completion % |
| `tackles` | int | Tackles made |
| `yellow_cards` | int | Yellow cards received |
| `red_cards` | int | Red cards received |
| `clean_sheets` | int | Clean sheets (GK/DEF only) |
| `rating` | float | Derived overall rating (5.0–9.5) |

**Rating formula:**
```
rating = clip(6.0 + goals×0.15 + assists×0.10 + (pass_accuracy−70)×0.02 + noise, 5.0, 9.5)
```

---

## 🔧 Regenerate the Dataset

To regenerate a fresh CSV (same seed = same output):

```bash
python generate_data.py
```

---

## 📄 License

MIT — free to use, modify, and distribute for personal or commercial projects.
