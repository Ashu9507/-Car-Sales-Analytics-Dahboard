import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════
st.set_page_config(
    page_title="AutoMetrics — Car Sales",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_URL = "http://localhost:8080/api/car_sales"
AI_URL   = "http://localhost:8080/api/ai/ask"

# ════════════════════════════════════════════
#  PREMIUM CSS & ANIMATIONS
# ════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap');

/* ── Global Styles & Animations ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    scroll-behavior: smooth;
}

::selection {
    background: rgba(59, 130, 246, 0.3);
    color: #F8FAFC;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #1E2235;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3B82F6;
}

/* Base App Background with subtle ambient glow */
.stApp {
    background-color: #05060A;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(59, 130, 246, 0.04), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(129, 140, 248, 0.04), transparent 25%);
}

/* Fade In Animation */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stMainBlockContainer"] {
    animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #08090E !important;
    border-right: 1px solid rgba(255,255,255,0.03) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; width: 1px;
    background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.05), transparent);
}

/* ── Premium Sidebar Navigation Menu ── */
[data-testid="stSidebar"] .stRadio > label { display: none !important; }
[data-testid="stSidebar"] [data-baseweb="radio"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    gap: 0 !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 14px 20px !important;
    border-radius: 10px !important;
    color: #64748B !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
    margin-bottom: 6px !important;
    border: 1px solid transparent !important;
    position: relative;
    overflow: hidden;
}

/* Hover State */
[data-testid="stSidebar"] [data-baseweb="radio"] label:hover {
    color: #E2E8F0 !important;
    background: rgba(255, 255, 255, 0.03) !important;
    transform: translateX(4px) !important;
}

/* Active State */
[data-testid="stSidebar"] [data-baseweb="radio"] [aria-checked="true"] ~ div,
[data-testid="stSidebar"] [data-baseweb="radio"] label:has([aria-checked="true"]) {
    background: linear-gradient(90deg, rgba(59, 130, 246, 0.12) 0%, rgba(59, 130, 246, 0.0) 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
    border-left: 3px solid #3B82F6 !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02) !important;
    transform: translateX(4px) !important;
}

/* Hide the native radio circle dot */
[data-testid="stSidebar"] [data-baseweb="radio"] [role="radio"] { display: none !important; }

/* ── Premium Glass Metrics ── */
[data-testid="metric-container"] {
    background: rgba(13, 15, 24, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 4px 24px -4px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    border-radius: 16px;
    padding: 24px 28px;
    position: relative;
    transition: transform 0.3s ease;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    border: 1px solid rgba(255,255,255,0.08);
}
[data-testid="metric-container"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,0.5), transparent);
}
[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-size: 12px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 34px !important;
    font-weight: 500 !important;
    letter-spacing: -0.02em !important;
    margin-top: 4px;
}

/* ── Input Controls ── */
[data-testid="stNumberInput"] input, textarea {
    background: rgba(13, 15, 24, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #F8FAFC !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 16px !important;
    transition: all 0.2s ease;
}
[data-testid="stNumberInput"] input:focus, textarea:focus {
    border-color: rgba(59, 130, 246, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15) !important;
}
textarea::placeholder { color: #475569 !important; }

/* ── Glowing AI Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2563EB, #4F46E5) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    padding: 12px 32px !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.3) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button:hover {
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
    transform: translateY(-1px) !important;
    filter: brightness(1.1);
}

/* ── Expanders & Dividers ── */
[data-testid="stExpander"] {
    background: rgba(13, 15, 24, 0.4) !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #94A3B8 !important;
    font-weight: 500 !important;
}
hr {
    border-color: rgba(255,255,255,0.04) !important;
    margin: 32px 0 !important;
}

/* Luxury Gradient Text Utility */
.gradient-text {
    background: linear-gradient(to right, #FFFFFF, #94A3B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  PLOTLY THEME UPGRADES
# ════════════════════════════════════════════
BG        = "rgba(0,0,0,0)"
GRID      = "rgba(255,255,255,0.03)"
TICK      = "#64748B"
ACCENT    = "#3B82F6"
ACCENT2   = "#818CF8"
CARD_BG   = "rgba(13, 15, 24, 0.6)"

def base_layout(**overrides):
    layout = dict(
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        font=dict(family="Inter, sans-serif", color=TICK),
        title_font=dict(family="Playfair Display, serif", color="#F8FAFC", size=22),
        title_x=0.02,
        title_pad=dict(l=0, t=10, b=25),
        margin=dict(l=10, r=10, t=65, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0.5)", 
            bordercolor="rgba(255,255,255,0.05)",
            borderwidth=1,
            font=dict(color="#94A3B8", size=12)
        ),
        xaxis=dict(
            gridcolor=GRID, zerolinecolor=GRID,
            tickfont=dict(color=TICK, size=12), linecolor="rgba(0,0,0,0)"
        ),
        yaxis=dict(
            gridcolor=GRID, zerolinecolor="rgba(0,0,0,0)",
            tickfont=dict(color=TICK, size=12), linecolor="rgba(0,0,0,0)"
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(15, 19, 32, 0.9)",
            bordercolor="rgba(255,255,255,0.1)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif", size=13)
        ),
    )
    layout.update(overrides)
    return layout

# ════════════════════════════════════════════
#  API FUNCTIONS
# ════════════════════════════════════════════
@st.cache_data(ttl=300)
def get_yearly_sales():
    try:
        r = requests.get(f"{BASE_URL}/yearly-count", timeout=10)
        r.raise_for_status()
        data = r.json()["data"]
        if isinstance(data, dict):
            data = [data]
        return pd.DataFrame(data)
    except Exception as e:
        return f"API is down : {e}"

@st.cache_data(ttl=300)
def get_monthly_sales(year: int):
    try:
        r = requests.get(f"{BASE_URL}/monthly-count", params={"year": year}, timeout=10)
        r.raise_for_status()
        data = r.json()["data"]
        if isinstance(data, dict):
            data = [data]
        return pd.DataFrame(data)
    except Exception as e:
        return f"API is down : {e}"
    
@st.cache_data(ttl=300)
def get_weekly_sales(year: int, month: int):
    try:
        r = requests.get(f"{BASE_URL}/weekly-count", params={"year": year,"month": month}, timeout=10)
        r.raise_for_status()
        data = r.json()["data"]
        if isinstance(data, dict):
            data = [data]
        return pd.DataFrame(data)
    except Exception as e:
        return f"API is down : {e}"

def ask_ai(question: str):
    try:
        r = requests.post(AI_URL, json=question, timeout=30)
        return r.text
    except Exception as e:
        return f"This is an AI placeholder. The backend endpoint was not reachable: {e}"

# ════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ════════════════════════════════════════════
st.sidebar.markdown("""
<div style="padding: 32px 20px 20px;">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
        <span style="font-size:24px;color:#3B82F6;text-shadow: 0 0 20px rgba(59,130,246,0.5);">◈</span>
        <span style="font-family:'Playfair Display',serif;font-size:22px;
                     color:#F8FAFC;font-weight:600;letter-spacing:-0.03em;">AutoMetrics</span>
    </div>
    <p style="font-size:12px;color:#64748B;margin:0;letter-spacing:0.02em;">
        Premium Sales Intelligence
    </p>
</div>
<div style="height:1px;background:linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);margin:0 20px 32px;"></div>
<div style="padding:0 24px; margin-bottom:12px;">
    <p style="font-size:11px;letter-spacing:0.2em;text-transform:uppercase;
              color:#64748B;font-weight:600;margin:0;display:flex;align-items:center;gap:10px;">
        <span style="width:16px;height:1px;background:rgba(59,130,246,0.5);"></span>
        Main Menu
    </p>
</div>
""", unsafe_allow_html=True)

option = st.sidebar.radio(
    "Navigation",
    ["Yearly Analytics", "Monthly Analytics", "Weekly Analytics", "AI Insights"],
    label_visibility="collapsed",
)

# ════════════════════════════════════════════
#  PAGE HEADER
# ════════════════════════════════════════════
HEADERS = {
    "Yearly Analytics":  ("Overview · Yearly",    "Sales Performance"),
    "Monthly Analytics": ("Overview · Monthly",   "Monthly Breakdown"),
    "Weekly Analytics": ("Overview · Weekly",   "Weekly Sales in each Monthly Breakdown"),
    "AI Insights":       ("Intelligence · AI",    "AI-Powered Insights"),
}
eyebrow, title = HEADERS[option]

st.markdown(f"""
<div style="padding: 24px 0 40px;">
    <p style="font-size:11px;letter-spacing:0.2em;text-transform:uppercase;
              color:#3B82F6;font-weight:600;margin:0 0 12px;">{eyebrow}</p>
    <h1 class="gradient-text" style="font-family:'Playfair Display',serif;
               font-size:42px;font-weight:600;margin:0;line-height:1.15;
               letter-spacing:-0.02em;">{title}</h1>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  CHART CARD HELPER
# ════════════════════════════════════════════
def chart_card(fig):
    st.markdown(f"""
    <div style="background:{CARD_BG}; backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
                border:1px solid rgba(255,255,255,0.05); box-shadow:0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04);
                border-radius:20px; padding:28px 24px 12px; margin-bottom:24px;">
    """, unsafe_allow_html=True)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════
#  YEARLY ANALYTICS
# ════════════════════════════════════════════
if option == "Yearly Analytics":

    with st.spinner("Compiling yearly data…"):
        df = get_yearly_sales()

    if df.empty:
        st.warning("No data returned from the API.")
        st.stop()

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Units Sold",  f"{df['count'].sum():,}")
    c2.metric("Peak Year",         f"{df.loc[df['count'].idxmax(), 'year']}")
    c3.metric("Peak Volume",       f"{df['count'].max():,}")
    c4.metric("Annual Average",    f"{int(df['count'].mean()):,}")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # Area line
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df["year"], y=df["count"],
        mode="lines+markers",
        line=dict(color=ACCENT, width=3, shape="spline", smoothing=1),
        marker=dict(size=8, color="#05060A", line=dict(color=ACCENT, width=2.5)),
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.1)",
        hovertemplate="<b>%{x}</b><br>Units sold: <span style='color:#ffffff'>%{y:,}</span><extra></extra>",
    ))
    fig1.update_layout(**base_layout(title="Volume Progression over Time"))
    chart_card(fig1)

    # Bar chart
    bar_colors = [ACCENT if c == df["count"].max() else "rgba(255,255,255,0.08)" for c in df["count"]]
    fig2 = go.Figure(go.Bar(
        x=df["year"], y=df["count"],
        text=df["count"], textposition="outside",
        textfont=dict(color="#94A3B8", size=12),
        marker=dict(color=bar_colors, line=dict(color="rgba(0,0,0,0)"), cornerradius=6),
        hovertemplate="<b>%{x}</b><br>Units: <span style='color:#ffffff'>%{y:,}</span><extra></extra>",
    ))
    fig2.update_layout(**base_layout(
        title="Year-by-Year Volume",
        bargap=0.4,
        yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, showticklabels=False)
    ))
    chart_card(fig2)

    with st.expander("Explore Raw Data"):
        st.dataframe(df.style.format({"count": "{:,}"}), width="stretch", hide_index=True)

# ════════════════════════════════════════════
#  MONTHLY ANALYTICS
# ════════════════════════════════════════════
elif option == "Monthly Analytics":

    year = st.number_input(
        "Select Reporting Year", min_value=2000, max_value=2100, value=2024,
        label_visibility="visible",
    )

    with st.spinner("Fetching monthly metrics…"):
        df = get_monthly_sales(int(year))

    if df.empty:
        st.warning("No data returned for this year.")
        st.stop()

    MONTH_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                 7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    df["month_name"] = df["month"].map(MONTH_MAP)

    # KPIs
    best = df.loc[df["count"].idxmax()]
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Units",   f"{df['count'].sum():,}")
    c2.metric("Best Month",    best["month_name"])
    c3.metric("Monthly Avg",   f"{int(df['count'].mean()):,}")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # Gradient bar
    palette = px.colors.sequential.Blues[2:]
    norm = (df["count"] - df["count"].min()) / (df["count"].max() - df["count"].min() + 1e-9)
    bcolors = [palette[min(int(v * (len(palette)-1)), len(palette)-1)] for v in norm]

    fig1 = go.Figure(go.Bar(
        x=df["month_name"], y=df["count"],
        text=df["count"], textposition="outside",
        textfont=dict(color="#94A3B8", size=12),
        marker=dict(color=bcolors, line=dict(color="rgba(0,0,0,0)"), cornerradius=6),
        hovertemplate="<b>%{x}</b><br>Units: <span style='color:#ffffff'>%{y:,}</span><extra></extra>",
    ))
    fig1.update_layout(**base_layout(title=f"Monthly Trajectory — {year}", bargap=0.35))
    chart_card(fig1)

    # Radial / Polar
    months = df["month_name"].tolist()
    counts = df["count"].tolist()
    fig2 = go.Figure(go.Scatterpolar(
        r=counts + [counts[0]],
        theta=months + [months[0]],
        fill="toself",
        fillcolor="rgba(59,130,246,0.15)",
        line=dict(color=ACCENT, width=2.5, shape="spline"),
        marker=dict(size=6, color="#ffffff", line=dict(color=ACCENT, width=2)),
        hovertemplate="<b>%{theta}</b><br>Units: <span style='color:#ffffff'>%{r:,}</span><extra></extra>",
    ))
    polar_layout = {k: v for k, v in base_layout().items() if k not in ("xaxis", "yaxis")}
    polar_layout.update(
        title=f"Seasonal Pattern Analysis",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(tickfont=dict(color="#94A3B8", size=12), gridcolor=GRID, linecolor="rgba(0,0,0,0)"),
            radialaxis=dict(tickfont=dict(color=TICK, size=10), gridcolor=GRID, showticklabels=False, linecolor="rgba(0,0,0,0)"),
        ),
    )
    fig2.update_layout(**polar_layout)
    chart_card(fig2)

    with st.expander("Explore Raw Data"):
        st.dataframe(df[["month_name", "count"]].style.format({"count": "{:,}"}), width="stretch", hide_index=True)


# ════════════════════════════════════════════
#  WEEKLY ANALYTICS OF EACH MONTH IN A YEAR
# ════════════════════════════════════════════
elif option == "Weekly Analytics":

    # Input Controls for Year and Month
    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input(
            "Select Reporting Year", min_value=2000, max_value=2100, value=2024,
            label_visibility="visible",
        )
    with col2:
        MONTH_OPTIONS = {
            1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June",
            7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"
        }
        month = st.selectbox(
            "Select Reporting Month", 
            options=list(MONTH_OPTIONS.keys()), 
            format_func=lambda x: MONTH_OPTIONS[x],
            index=2 # Default to March
        )

    with st.spinner("Compiling weekly data…"):
        df = get_weekly_sales(int(year), int(month))

    if df.empty:
        st.warning(f"No data returned for {MONTH_OPTIONS[month]} {int(year)}.")
        st.stop()

    # Format the 'week' column for better visualization
    df["week_label"] = "Week " + df["week"].astype(str)

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Units Sold",  f"{df['count'].sum():,}")
    c2.metric("Peak Week",         f"{df.loc[df['count'].idxmax(), 'week_label']}")
    c3.metric("Peak Volume",       f"{df['count'].max():,}")

    st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

    # ── Premium Split Layout ──
    chart_col1, chart_col2 = st.columns([6, 4]) # 60% width for Combo, 40% for Donut

    with chart_col1:
        # Combo Chart: Bar + Line
        fig1 = go.Figure()
        
        # Bars for Volume
        fig1.add_trace(go.Bar(
            x=df["week_label"], y=df["count"],
            name="Volume",
            text=df["count"], textposition="outside",
            textfont=dict(color="#94A3B8", size=12),
            marker=dict(color="rgba(59,130,246,0.15)", line=dict(color=ACCENT, width=1), cornerradius=4),
            hovertemplate="<b>%{x}</b><br>Units: %{y:,}<extra></extra>",
        ))
        
        # Line for Trend Trajectory
        fig1.add_trace(go.Scatter(
            x=df["week_label"], y=df["count"],
            name="Trend",
            mode="lines+markers",
            line=dict(color="#818CF8", width=3, shape="spline", smoothing=1),
            marker=dict(size=8, color="#05060A", line=dict(color="#818CF8", width=2.5)),
            hovertemplate="<extra></extra>", # Hide hover to prevent double tooltips
        ))

        fig1.update_layout(**base_layout(
            title=f"Volume & Trend — {MONTH_OPTIONS[month]} {int(year)}",
            bargap=0.4,
            showlegend=False,
            yaxis=dict(showgrid=True, gridcolor=GRID, zeroline=False, showticklabels=False)
        ))
        chart_card(fig1)

    with chart_col2:
        # Donut Chart: Weekly Contribution
        fig2 = go.Figure(go.Pie(
            labels=df["week_label"],
            values=df["count"],
            hole=0.65,
            marker=dict(
                colors=["#1E3A8A", "#2563EB", "#3B82F6", "#60A5FA", "#93C5FD"],
                line=dict(color="#05060A", width=2)
            ),
            textinfo="percent",
            textfont=dict(size=14, color="#FFFFFF", family="Inter"),
            hovertemplate="<b>%{label}</b><br>Units: %{value} (%{percent})<extra></extra>"
        ))
        
        fig2.update_layout(**base_layout(
            title="Weekly Share",
            margin=dict(l=10, r=10, t=65, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, bgcolor="rgba(0,0,0,0)")
        ))
        
        # Add a central annotation for total
        fig2.add_annotation(
            text=f"<span style='font-size:24px; font-family:Playfair Display; color:#F8FAFC'>{df['count'].sum()}</span><br><span style='font-size:10px; color:#64748B; text-transform:uppercase'>Total</span>",
            x=0.5, y=0.5, showarrow=False
        )
        chart_card(fig2)

    with st.expander("Explore Raw Data"):
        st.dataframe(df[["week", "week_label", "count"]].style.format({"count": "{:,}"}), width="stretch", hide_index=True)

# ════════════════════════════════════════════
#  AI INSIGHTS
# ════════════════════════════════════════════
elif option == "AI Insights":

    st.markdown(f"""
    <div style="background:rgba(13, 15, 24, 0.4); backdrop-filter:blur(10px); -webkit-backdrop-filter:blur(10px);
                border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:28px 32px; margin-bottom:32px;
                border-left:4px solid {ACCENT}; box-shadow:0 10px 30px rgba(0,0,0,0.2);">
        <h3 style="font-family:'Playfair Display',serif; color:#F8FAFC; margin:0 0 12px 0; font-size:20px;">Natural Language Querying</h3>
        <p style="font-size:14px; color:#94A3B8; margin:0; line-height:1.6;">
            Ask complex questions about your car sales data directly. Your queries are processed via the 
            Spring Boot AI endpoint and insights are returned in real-time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "Ask a question",
        placeholder="e.g., Which year showed the most aggressive sales growth and why?",
        height=140,
        label_visibility="collapsed",
    )

    if st.button("Generate Insight  ✦"):
        if not question.strip():
            st.warning("Please enter a question to analyze.")
        else:
            with st.spinner("Analyzing data patterns…"):
                answer = ask_ai(question)

            st.markdown(f"""
            <div style="background:linear-gradient(180deg, rgba(13, 15, 24, 0.8), rgba(8, 9, 14, 0.9));
                        border:1px solid rgba(255,255,255,0.08); border-top:1px solid rgba(129, 140, 248, 0.4);
                        border-radius:16px; padding:32px; margin-top:32px; box-shadow:0 20px 40px rgba(0,0,0,0.4);">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:20px;">
                    <span style="color:#818CF8; font-size:18px;">✦</span>
                    <p style="font-size:11px; letter-spacing:0.2em; text-transform:uppercase;
                              color:#818CF8; font-weight:600; margin:0;">AI Analysis</p>
                </div>
                <div style="color:#E2E8F0; font-size:15px; line-height:1.75; font-family:'Inter', sans-serif;">
                    {answer}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════
st.markdown("""
<div style="margin-top:64px; padding-top:24px;
            border-top:1px solid rgba(255,255,255,0.04);
            display:flex; justify-content:space-between; align-items:center;">
    <span style="font-size:12px; color:#475569; letter-spacing:0.05em; font-weight:500;">
        ◈ AutoMetrics &nbsp;·&nbsp; Data Intelligence
    </span>
    <span style="font-size:12px; color:#475569;">
        Built by <span style="color:#64748B;">Ashutosh Kumar</span>
    </span>
</div>
""", unsafe_allow_html=True)