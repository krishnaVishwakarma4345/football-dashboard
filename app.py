"""
Football Player Performance Analytics Dashboard
================================================
A Streamlit application for interactive football player analysis.

NOTE: All data displayed is SYNTHETIC and does not represent
      real-world football player statistics.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
CSV_PATH = "football_players.csv"
POSITION_ORDER = ["GK", "DEF", "MID", "FWD"]
POSITION_COLORS = {
    "GK":  "#f5a623",
    "DEF": "#4a90d9",
    "MID": "#7ed321",
    "FWD": "#e84040",
}
PLOTLY_TEMPLATE = "plotly_dark"
BG_COLOR = "#0e1117"
CARD_BG = "#1e3a2f"
ACCENT = "#00ff88"

# ─────────────────────────────────────────────
# DATA GENERATION
# ─────────────────────────────────────────────
def generate_dataset(filepath: str = CSV_PATH) -> pd.DataFrame:
    """Create a reproducible synthetic football dataset and save to CSV."""
    rng = np.random.default_rng(42)

    TEAMS = [
        "FC Ironforge", "Redstone United", "Silverport Athletic", "Ashvale City",
        "Thornwick FC", "Crestfall Rovers", "Blackmoor United", "Goldenhaven SC",
        "Eastbridge FC", "Norwick Town",
    ]
    SEASONS = ["2021-22", "2022-23", "2023-24"]
    POSITIONS = ["GK", "DEF", "MID", "FWD"]
    POS_WEIGHTS = [0.08, 0.30, 0.35, 0.27]

    FIRST_NAMES = [
        "James", "Carlos", "Luca", "Antoine", "Rafael", "Marco", "David", "Oliver",
        "Gabriel", "Sergio", "Thomas", "Kevin", "Alexis", "Mohamed", "Pierre",
        "Roberto", "Fernando", "Jordi", "Kai", "Leon", "Emre", "Takumi", "Son",
        "Bruno", "Ederson", "Thibaut", "Virgil", "Sadio", "Raheem", "Wilfried",
        "Riyad", "Bernardo", "João", "Rodri", "İlkay", "Aymeric", "Kyle", "John",
        "Leroy", "Phil", "Jack", "Declan", "Mason", "Jadon", "Bukayo", "Emile",
        "Callum", "Patrick", "Richarlison", "Casemiro",
    ]
    LAST_NAMES = [
        "Hargreaves", "Mendez", "Ferretti", "Dubois", "Silva", "Rossi", "Müller",
        "Hernández", "Santos", "García", "Schmidt", "Dupont", "Fischer", "Martínez",
        "Andersen", "Johansson", "Nielsen", "Kovač", "Novak", "Popović", "Ivanov",
        "Petrov", "Sørensen", "Magnusson", "O'Brien", "Murphy", "Walsh", "Ryan",
        "Nkosi", "Diallo", "Touré", "Kante", "Mbeki", "Osei", "Kamara", "Traoré",
        "Nakamura", "Tanaka", "Yamamoto", "Park", "Kim", "Lee", "Alves", "Costa",
        "Pereira", "Oliveira", "Gomes", "Sousa", "Fernandes", "Carvalho",
    ]

    records = []
    player_id = 1
    for team in TEAMS:
        for season in SEASONS:
            n_players = rng.integers(13, 16)
            positions = rng.choice(POSITIONS, size=n_players, p=POS_WEIGHTS)
            for pos in positions:
                name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
                age = int(rng.integers(17, 37))
                matches = int(rng.integers(5, 39))
                minutes = int(matches * rng.integers(30, 91))

                if pos == "GK":
                    goals, assists = int(rng.poisson(0.1)), int(rng.poisson(0.2))
                    shots = int(goals * rng.integers(1, 4)) if goals > 0 else 0
                    passes = int(rng.integers(200, 600))
                    pass_acc = float(round(rng.normal(68, 5), 1))
                    tackles = int(rng.integers(0, 10))
                    clean_sheets = int(rng.integers(0, min(matches, 20) + 1))
                elif pos == "DEF":
                    goals, assists = int(rng.poisson(1.2)), int(rng.poisson(1.5))
                    shots = int(goals * rng.integers(2, 6)) if goals > 0 else int(rng.integers(0, 5))
                    passes = int(rng.integers(400, 900))
                    pass_acc = float(round(rng.normal(75, 5), 1))
                    tackles = int(rng.integers(20, 80))
                    clean_sheets = int(rng.integers(0, min(matches // 2, 15) + 1))
                elif pos == "MID":
                    goals, assists = int(rng.poisson(3.5)), int(rng.poisson(4.5))
                    shots = int(goals * rng.integers(3, 7)) if goals > 0 else int(rng.integers(2, 15))
                    passes = int(rng.integers(600, 1400))
                    pass_acc = float(round(rng.normal(80, 5), 1))
                    tackles = int(rng.integers(10, 60))
                    clean_sheets = 0
                else:
                    goals, assists = int(rng.poisson(8.0)), int(rng.poisson(3.5))
                    shots = int(goals * rng.integers(3, 8)) if goals > 0 else int(rng.integers(5, 25))
                    passes = int(rng.integers(150, 600))
                    pass_acc = float(round(rng.normal(72, 6), 1))
                    tackles = int(rng.integers(2, 25))
                    clean_sheets = 0

                sot_lo = max(1, int(shots * 0.3))
                sot_hi = max(2, int(shots * 0.7) + 1)
                shots_on_target = int(min(shots, rng.integers(sot_lo, sot_hi)))
                pass_acc = float(np.clip(pass_acc, 50.0, 98.0))
                yellow_cards = int(rng.poisson(0.8))
                red_cards = int(rng.poisson(0.05))

                rating = float(round(np.clip(
                    6.0 + goals * 0.15 + assists * 0.10
                    + (pass_acc - 70) * 0.02 + float(rng.normal(0, 0.3)),
                    5.0, 9.5
                ), 2))

                records.append({
                    "player_id": player_id, "player_name": name, "team": team,
                    "position": pos, "season": season, "age": age,
                    "matches_played": matches, "minutes_played": minutes,
                    "goals": goals, "assists": assists, "shots": shots,
                    "shots_on_target": shots_on_target, "passes": passes,
                    "pass_accuracy": pass_acc, "tackles": tackles,
                    "yellow_cards": yellow_cards, "red_cards": red_cards,
                    "clean_sheets": clean_sheets, "rating": rating,
                })
                player_id += 1

    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    return df


# ─────────────────────────────────────────────
# DATA LOADING & VALIDATION
# ─────────────────────────────────────────────
REQUIRED_COLUMNS = [
    "player_id", "player_name", "team", "position", "season", "age",
    "matches_played", "minutes_played", "goals", "assists", "shots",
    "shots_on_target", "passes", "pass_accuracy", "tackles",
    "yellow_cards", "red_cards", "clean_sheets", "rating",
]
NUMERIC_COLUMNS = [
    "age", "matches_played", "minutes_played", "goals", "assists",
    "shots", "shots_on_target", "passes", "pass_accuracy", "tackles",
    "yellow_cards", "red_cards", "clean_sheets", "rating",
]


@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        generate_dataset(CSV_PATH)

    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        st.error(f"❌ Could not read '{CSV_PATH}': {e}")
        st.stop()

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        st.error(f"❌ Dataset is missing required columns: {missing}")
        st.stop()

    # Coerce numerics, drop unrecoverable rows
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df.dropna(subset=NUMERIC_COLUMNS, inplace=True)
    dropped = before - len(df)
    if dropped > 0:
        st.sidebar.warning(f"⚠️ {dropped} row(s) with missing values were excluded.")

    df["position"] = df["position"].str.upper().str.strip()
    return df


# ─────────────────────────────────────────────
# CSS INJECTION
# ─────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
    <style>
    /* ── Main background ── */
    .stApp { background-color: #0e1117; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] { background-color: #1a1f2e; }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 { color: #00ff88; }

    /* ── KPI card ── */
    .kpi-card {
        background: #1e3a2f;
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 18px 14px;
        text-align: center;
        margin-bottom: 10px;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #8b9daa;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #00ff88;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: #6a7d8b;
        margin-top: 4px;
    }

    /* ── Section headers ── */
    .section-header {
        color: #00ff88;
        font-size: 1.15rem;
        font-weight: 600;
        border-left: 4px solid #00ff88;
        padding-left: 10px;
        margin: 22px 0 12px 0;
    }

    /* ── Synthetic data banner ── */
    .synthetic-banner {
        background: #2a1f0e;
        border: 1px solid #f5a623;
        border-radius: 8px;
        padding: 8px 14px;
        color: #f5a623;
        font-size: 0.8rem;
        margin-bottom: 14px;
    }

    /* ── Tab styling ── */
    [data-testid="stTabs"] button { color: #8b9daa !important; font-size: 0.95rem; }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #00ff88 !important;
        border-bottom: 2px solid #00ff88;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] { border: 1px solid #2a3040; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Football_Pallo_valkoinen.svg/"
        "240px-Football_Pallo_valkoinen.svg.png",
        width=60,
    )
    st.sidebar.markdown("## ⚽ Dashboard Filters")
    st.sidebar.markdown("---")

    # Season
    all_seasons = sorted(df["season"].unique())
    seasons = st.sidebar.multiselect("📅 Season", all_seasons, default=all_seasons)

    # Team
    all_teams = sorted(df["team"].unique())
    teams = st.sidebar.multiselect("🏟️ Team", all_teams, default=all_teams)

    # Position
    all_positions = [p for p in POSITION_ORDER if p in df["position"].unique()]
    positions = st.sidebar.multiselect("🎽 Position", all_positions, default=all_positions)

    # Player search
    player_search = st.sidebar.text_input("🔍 Search Player Name", placeholder="e.g. Carlos")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='color:#6a7d8b;font-size:0.75rem;'>⚠️ <b>Synthetic data only.</b><br>"
        "Does not represent real football statistics.</div>",
        unsafe_allow_html=True,
    )

    # Apply filters
    filtered = df.copy()
    if seasons:
        filtered = filtered[filtered["season"].isin(seasons)]
    if teams:
        filtered = filtered[filtered["team"].isin(teams)]
    if positions:
        filtered = filtered[filtered["position"].isin(positions)]
    if player_search.strip():
        filtered = filtered[
            filtered["player_name"].str.contains(player_search.strip(), case=False, na=False)
        ]

    return filtered


def check_empty(df: pd.DataFrame) -> bool:
    """Return True (and show warning) if DataFrame is empty."""
    if df.empty:
        st.warning("⚠️ No players match the current filters. Adjust the sidebar selections.")
        return True
    return False


# ─────────────────────────────────────────────
# HELPER: standard figure layout
# ─────────────────────────────────────────────
def style_fig(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_COLOR,
        plot_bgcolor="#12171f",
        height=height,
        margin=dict(l=40, r=20, t=50, b=40),
        font=dict(family="sans-serif", size=12, color="#c0ccd6"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_color="#c0ccd6"),
    )
    fig.update_xaxes(gridcolor="#1e2733", zerolinecolor="#1e2733")
    fig.update_yaxes(gridcolor="#1e2733", zerolinecolor="#1e2733")
    return fig


# ─────────────────────────────────────────────
# SUB-TASK 3 — OVERVIEW PAGE
# ─────────────────────────────────────────────
def render_kpi_cards(df: pd.DataFrame) -> None:
    total_players   = df["player_id"].nunique()
    total_goals     = int(df["goals"].sum())
    total_assists   = int(df["assists"].sum())
    total_minutes   = int(df["minutes_played"].sum())
    avg_rating      = round(float(df["rating"].mean()), 2)

    cols = st.columns(5)
    cards = [
        ("👥 Total Players",     f"{total_players:,}",        "unique player records"),
        ("⚽ Total Goals",        f"{total_goals:,}",          "across all matches"),
        ("🎯 Total Assists",      f"{total_assists:,}",        "across all matches"),
        ("⏱️ Minutes Played",    f"{total_minutes:,}",        "combined minutes"),
        ("⭐ Avg Rating",         f"{avg_rating}",             "out of 9.5"),
    ]
    for col, (label, value, sub) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="kpi-card">'
                f'<div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div>'
                f'<div class="kpi-sub">{sub}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def render_overview_page(df: pd.DataFrame) -> None:
    st.markdown('<div class="synthetic-banner">⚠️ All statistics below are <b>synthetic / simulated</b> and do not represent real-world football data.</div>', unsafe_allow_html=True)
    render_kpi_cards(df)

    st.markdown('<div class="section-header">🏆 Top 10 Players by Rating</div>', unsafe_allow_html=True)
    top10 = (
        df.sort_values("rating", ascending=False)
        .drop_duplicates("player_name")
        .head(10)
        .sort_values("rating")
    )
    fig_top = go.Figure(go.Bar(
        x=top10["rating"],
        y=top10["player_name"],
        orientation="h",
        marker=dict(
            color=top10["rating"],
            colorscale=[[0, "#1e3a2f"], [0.5, "#00aa55"], [1, "#00ff88"]],
            showscale=False,
        ),
        text=top10["rating"].astype(str),
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Rating: %{x}<br>Team: " +
                      top10["team"].values.tolist().__str__() + "<extra></extra>",
    ))
    fig_top.update_layout(
        xaxis=dict(range=[4.5, 10], title="Rating"),
        yaxis=dict(title=""),
        title="Top 10 Players — Overall Rating",
    )
    # Rebuild hover with actual team values
    fig_top = go.Figure(go.Bar(
        x=top10["rating"],
        y=top10["player_name"],
        orientation="h",
        marker=dict(
            color=top10["rating"],
            colorscale=[[0, "#1e3a2f"], [0.5, "#00aa55"], [1, "#00ff88"]],
            showscale=False,
        ),
        text=top10["rating"],
        textposition="outside",
        customdata=np.stack([top10["team"].values, top10["position"].values], axis=-1),
        hovertemplate="<b>%{y}</b><br>Rating: %{x}<br>Team: %{customdata[0]}<br>Position: %{customdata[1]}<extra></extra>",
    ))
    fig_top.update_layout(xaxis=dict(range=[4.5, 10], title="Rating"), yaxis_title="")
    st.plotly_chart(style_fig(fig_top, 400), use_container_width=True)

    st.markdown('<div class="section-header">📊 Goals Distribution by Position</div>', unsafe_allow_html=True)
    fig_hist = px.histogram(
        df, x="goals", color="position",
        color_discrete_map=POSITION_COLORS,
        barmode="overlay",
        opacity=0.75,
        labels={"goals": "Goals Scored", "count": "Number of Players"},
        title="Goals Distribution by Position",
        category_orders={"position": POSITION_ORDER},
    )
    fig_hist.update_traces(hovertemplate="Goals: %{x}<br>Count: %{y}<extra></extra>")
    st.plotly_chart(style_fig(fig_hist), use_container_width=True)


# ─────────────────────────────────────────────
# SUB-TASK 4 — PLAYER ANALYSIS PAGE
# ─────────────────────────────────────────────
def render_player_analysis_page(df: pd.DataFrame) -> None:
    st.markdown('<div class="synthetic-banner">⚠️ Synthetic data only — not real player statistics.</div>', unsafe_allow_html=True)

    # ── Player Comparison Radar ──
    st.markdown('<div class="section-header">🕸️ Player Comparison Radar</div>', unsafe_allow_html=True)
    all_names = sorted(df["player_name"].unique())
    default_names = all_names[:min(3, len(all_names))]
    selected = st.multiselect(
        "Select up to 5 players to compare",
        options=all_names,
        default=default_names,
        max_selections=5,
    )

    if len(selected) < 2:
        st.info("ℹ️ Select at least 2 players to display the radar chart.")
    else:
        RADAR_STATS = ["goals", "assists", "pass_accuracy", "tackles", "rating"]
        RADAR_LABELS = ["Goals", "Assists", "Pass Acc.", "Tackles", "Rating"]

        # Normalise each stat to 0–1 using dataset-wide min/max
        stat_min = df[RADAR_STATS].min()
        stat_max = df[RADAR_STATS].max()
        stat_range = (stat_max - stat_min).replace(0, 1)

        fig_radar = go.Figure()
        palette = ["#00ff88", "#4a90d9", "#f5a623", "#e84040", "#c678dd"]
        for i, player in enumerate(selected):
            player_row = df[df["player_name"] == player].iloc[0]
            norm = [(player_row[s] - stat_min[s]) / stat_range[s] for s in RADAR_STATS]
            norm += [norm[0]]  # close polygon
            labels = RADAR_LABELS + [RADAR_LABELS[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=norm, theta=labels, fill="toself",
                name=player, line=dict(color=palette[i % len(palette)]),
                opacity=0.75,
                hovertemplate="<b>" + player + "</b><br>%{theta}<extra></extra>",
            ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#12171f",
                radialaxis=dict(visible=True, range=[0, 1], showticklabels=False, gridcolor="#2a3040"),
                angularaxis=dict(gridcolor="#2a3040"),
            ),
            showlegend=True,
            title="Player Comparison (Normalised Stats)",
        )
        st.plotly_chart(style_fig(fig_radar, 480), use_container_width=True)

    # ── Goals vs Assists Scatter ──
    st.markdown('<div class="section-header">⚽ Goals vs Assists</div>', unsafe_allow_html=True)
    fig_ga = px.scatter(
        df, x="goals", y="assists",
        color="position",
        color_discrete_map=POSITION_COLORS,
        size="minutes_played",
        size_max=22,
        hover_name="player_name",
        hover_data={"team": True, "rating": True, "season": True, "minutes_played": False, "position": False},
        labels={"goals": "Goals", "assists": "Assists"},
        title="Goals vs Assists (size = minutes played)",
        category_orders={"position": POSITION_ORDER},
    )
    fig_ga.update_traces(marker=dict(opacity=0.75, line=dict(width=0.5, color="#0e1117")))
    st.plotly_chart(style_fig(fig_ga), use_container_width=True)

    # ── Shots vs Goals Scatter ──
    st.markdown('<div class="section-header">🎯 Shots vs Goals (Conversion Efficiency)</div>', unsafe_allow_html=True)
    plot_df = df.copy()
    plot_df["conversion_rate"] = np.where(
        plot_df["shots"] > 0,
        (plot_df["goals"] / plot_df["shots"] * 100).round(1),
        0.0,
    )
    fig_sg = px.scatter(
        plot_df, x="shots", y="goals",
        color="position",
        color_discrete_map=POSITION_COLORS,
        hover_name="player_name",
        hover_data={"team": True, "conversion_rate": True, "season": True, "position": False},
        labels={"shots": "Total Shots", "goals": "Goals Scored", "conversion_rate": "Conversion %"},
        title="Shots vs Goals — Shot Conversion Efficiency",
        category_orders={"position": POSITION_ORDER},
    )
    fig_sg.update_traces(
        marker=dict(opacity=0.7, line=dict(width=0.5, color="#0e1117")),
    )
    # Manual linear trendline using NumPy (no statsmodels required)
    x_vals = plot_df["shots"].values
    y_vals = plot_df["goals"].values
    valid = (x_vals >= 0) & (y_vals >= 0)
    if valid.sum() > 1:
        coeffs = np.polyfit(x_vals[valid], y_vals[valid], deg=1)
        x_line = np.linspace(x_vals[valid].min(), x_vals[valid].max(), 200)
        y_line = np.polyval(coeffs, x_line)
        fig_sg.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode="lines",
            line=dict(color=ACCENT, width=2, dash="dash"),
            name="Trend (linear)",
            hovertemplate="Trend<br>Shots: %{x:.0f}<br>Predicted Goals: %{y:.1f}<extra></extra>",
        ))
    st.plotly_chart(style_fig(fig_sg), use_container_width=True)


# ─────────────────────────────────────────────
# SUB-TASK 5 — TEAM ANALYSIS PAGE
# ─────────────────────────────────────────────
def render_team_analysis_page(df: pd.DataFrame) -> None:
    st.markdown('<div class="synthetic-banner">⚠️ Synthetic data only — not real club statistics.</div>', unsafe_allow_html=True)

    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            player_count=("player_id", "nunique"),
            avg_rating=("rating", "mean"),
        )
        .round({"avg_rating": 2})
    )

    # ── Goals & Assists grouped bar ──
    st.markdown('<div class="section-header">⚽ Goals & Assists by Team</div>', unsafe_allow_html=True)
    team_sorted = team_agg.sort_values("total_goals", ascending=False)
    fig_ga = go.Figure([
        go.Bar(name="Goals",   x=team_sorted["team"], y=team_sorted["total_goals"],
               marker_color="#00ff88",
               hovertemplate="<b>%{x}</b><br>Goals: %{y}<extra></extra>"),
        go.Bar(name="Assists", x=team_sorted["team"], y=team_sorted["total_assists"],
               marker_color="#4a90d9",
               hovertemplate="<b>%{x}</b><br>Assists: %{y}<extra></extra>"),
    ])
    fig_ga.update_layout(barmode="group", xaxis_tickangle=-35, title="Team Goals & Assists")
    st.plotly_chart(style_fig(fig_ga, 420), use_container_width=True)

    col1, col2 = st.columns(2)

    # ── Player count ──
    with col1:
        st.markdown('<div class="section-header">👥 Players per Team</div>', unsafe_allow_html=True)
        pc = team_agg.sort_values("player_count")
        fig_pc = go.Figure(go.Bar(
            x=pc["player_count"], y=pc["team"], orientation="h",
            marker_color="#7ed321",
            hovertemplate="<b>%{y}</b><br>Players: %{x}<extra></extra>",
        ))
        fig_pc.update_layout(xaxis_title="Unique Players", yaxis_title="", title="Player Count")
        st.plotly_chart(style_fig(fig_pc, 380), use_container_width=True)

    # ── Avg rating ──
    with col2:
        st.markdown('<div class="section-header">⭐ Average Rating by Team</div>', unsafe_allow_html=True)
        ar = team_agg.sort_values("avg_rating", ascending=False)
        fig_ar = go.Figure(go.Bar(
            x=ar["team"], y=ar["avg_rating"],
            marker=dict(
                color=ar["avg_rating"],
                colorscale=[[0, "#1e3a2f"], [0.5, "#00aa55"], [1, "#00ff88"]],
                showscale=False,
            ),
            text=ar["avg_rating"].round(2),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Avg Rating: %{y}<extra></extra>",
        ))
        fig_ar.update_layout(
            xaxis_tickangle=-35,
            yaxis=dict(range=[5, 9.5], title="Avg Rating"),
            title="Team Average Rating",
        )
        st.plotly_chart(style_fig(fig_ar, 380), use_container_width=True)


# ─────────────────────────────────────────────
# SUB-TASK 6 — POSITION ANALYSIS PAGE
# ─────────────────────────────────────────────
def render_position_analysis_page(df: pd.DataFrame) -> None:
    st.markdown('<div class="synthetic-banner">⚠️ Synthetic data only — not real positional statistics.</div>', unsafe_allow_html=True)

    pos_agg = (
        df.groupby("position", as_index=False)
        .agg(
            total_goals=("goals", "sum"),
            total_assists=("assists", "sum"),
            avg_rating=("rating", "mean"),
            clean_sheets=("clean_sheets", "sum"),
        )
        .round({"avg_rating": 2})
    )
    # Ensure consistent order
    pos_agg["position"] = pd.Categorical(pos_agg["position"], categories=POSITION_ORDER, ordered=True)
    pos_agg = pos_agg.sort_values("position")

    # ── Grouped bar: goals + assists + rating ──
    st.markdown('<div class="section-header">📊 Goals, Assists & Avg Rating by Position</div>', unsafe_allow_html=True)
    fig_pos = go.Figure([
        go.Bar(name="Goals",      x=pos_agg["position"], y=pos_agg["total_goals"],
               marker_color="#00ff88",
               hovertemplate="<b>%{x}</b><br>Goals: %{y}<extra></extra>"),
        go.Bar(name="Assists",    x=pos_agg["position"], y=pos_agg["total_assists"],
               marker_color="#4a90d9",
               hovertemplate="<b>%{x}</b><br>Assists: %{y}<extra></extra>"),
        go.Bar(name="Avg Rating (×10)", x=pos_agg["position"], y=(pos_agg["avg_rating"] * 10).round(1),
               marker_color="#f5a623",
               hovertemplate="<b>%{x}</b><br>Avg Rating: %{customdata}<extra></extra>",
               customdata=pos_agg["avg_rating"]),
    ])
    fig_pos.update_layout(barmode="group", title="Stats by Position")
    st.plotly_chart(style_fig(fig_pos, 400), use_container_width=True)

    col1, col2 = st.columns(2)

    # ── Rating box plot ──
    with col1:
        st.markdown('<div class="section-header">📦 Rating Distribution by Position</div>', unsafe_allow_html=True)
        fig_box = px.box(
            df, x="position", y="rating",
            color="position",
            color_discrete_map=POSITION_COLORS,
            points="outliers",
            labels={"rating": "Player Rating", "position": "Position"},
            title="Rating Spread by Position",
            category_orders={"position": POSITION_ORDER},
        )
        fig_box.update_traces(hovertemplate="%{y:.2f}<extra></extra>")
        st.plotly_chart(style_fig(fig_box, 400), use_container_width=True)

    # ── Clean sheets ──
    with col2:
        st.markdown('<div class="section-header">🧤 Clean Sheets (GK & DEF)</div>', unsafe_allow_html=True)
        cs_df = pos_agg[pos_agg["position"].isin(["GK", "DEF"])]
        if cs_df.empty:
            st.info("No GK or DEF data in current filter selection.")
        else:
            fig_cs = go.Figure(go.Bar(
                x=cs_df["position"], y=cs_df["clean_sheets"],
                marker_color=["#f5a623", "#4a90d9"],
                text=cs_df["clean_sheets"],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Clean Sheets: %{y}<extra></extra>",
            ))
            fig_cs.update_layout(yaxis_title="Total Clean Sheets", title="Clean Sheets by Position")
            st.plotly_chart(style_fig(fig_cs, 400), use_container_width=True)


# ─────────────────────────────────────────────
# SUB-TASK 7 — STATS TABLE & CSV DOWNLOAD
# ─────────────────────────────────────────────
_table_call_count = 0

def render_stats_table(df: pd.DataFrame) -> None:
    global _table_call_count
    _table_call_count += 1
    table_key = f"table_search_{_table_call_count}"

    st.markdown("---")
    st.markdown('<div class="section-header">📋 Player Statistics Table</div>', unsafe_allow_html=True)

    col_search, col_btn = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 Search player in table", placeholder="e.g. Silva", key=table_key)
    with col_btn:
        st.markdown("<div style='padding-top:28px'></div>", unsafe_allow_html=True)
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_bytes,
            file_name="football_players_filtered.csv",
            mime="text/csv",
            key=f"download_csv_{_table_call_count}",
        )

    display_df = df.copy()
    if search.strip():
        display_df = display_df[
            display_df["player_name"].str.contains(search.strip(), case=False, na=False)
        ]

    if display_df.empty:
        st.warning("No players found for the table search term.")
    else:
        # Pretty column labels
        col_map = {
            "player_id": "ID", "player_name": "Player", "team": "Team",
            "position": "Pos", "season": "Season", "age": "Age",
            "matches_played": "MP", "minutes_played": "Mins",
            "goals": "G", "assists": "A", "shots": "Sh",
            "shots_on_target": "SoT", "passes": "Passes",
            "pass_accuracy": "Pass%", "tackles": "Tkl",
            "yellow_cards": "YC", "red_cards": "RC",
            "clean_sheets": "CS", "rating": "Rating",
        }
        styled = display_df.rename(columns=col_map)
        st.dataframe(
            styled,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "Rating": st.column_config.ProgressColumn(
                    "Rating", min_value=5.0, max_value=9.5, format="%.2f"
                ),
                "Pass%": st.column_config.NumberColumn("Pass%", format="%.1f%%"),
            },
        )
        st.caption(f"Showing {len(display_df):,} of {len(df):,} records.")


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────
def main() -> None:
    st.set_page_config(
        page_title="⚽ Football Analytics Dashboard",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    # Load & validate data (generates CSV if absent)
    df_full = load_data()

    # Sidebar filters → filtered DataFrame
    df = render_sidebar(df_full)

    # Header
    st.markdown(
        "<h1 style='color:#00ff88;margin-bottom:2px;'>⚽ Football Player Performance Analytics</h1>"
        "<p style='color:#6a7d8b;margin-top:0;font-size:0.9rem;'>Interactive dashboard — "
        f"{len(df_full):,} synthetic player records across 10 clubs & 3 seasons</p>",
        unsafe_allow_html=True,
    )

    if check_empty(df):
        return

    # Page tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "👤 Player Analysis",
        "🏟️ Team Analysis",
        "🎽 Position Analysis",
    ])

    with tab1:
        render_overview_page(df)
        render_stats_table(df)

    with tab2:
        render_player_analysis_page(df)
        render_stats_table(df)

    with tab3:
        render_team_analysis_page(df)
        render_stats_table(df)

    with tab4:
        render_position_analysis_page(df)
        render_stats_table(df)


if __name__ == "__main__":
    main()
