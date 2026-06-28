import io
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# 1. Page configuration & Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="InsightIQ | Data Refinery", 
    page_icon="🧭", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    /* Bento Grid Dark Theme */
    --bg-app: #09090B;        /* Deepest zinc black for background */
    --bg-bento: #18181B;      /* Lighter zinc for bento cards */
    --ink: #FAFAFA;           /* Off-white text */
    --ink-muted: #A1A1AA;     /* Muted zinc text */
    --accent: #38BDF8;        /* Sky blue accent */
    --accent-hover: #0284C7;
    --border: #27272A;        /* Subtle border lines */
    --radius-bento: 24px;     /* Massive radius for the bento look */
    --radius-sm: 12px;
}

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; background-color: var(--bg-app); color: var(--ink); }
.stApp { background-color: var(--bg-app); }

/* --- FIX NATIVE STREAMLIT TEXT COLORS --- */
h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stText, span { color: var(--ink) !important; }
p, .st-emotion-cache-1wivap2 { color: var(--ink-muted) !important; } /* Mute standard paragraphs slightly */
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.5px; }

/* --- BENTO GRID COMPONENT OVERRIDES --- */

/* 1. Metrics (The small stat boxes) */
[data-testid="metric-container"] {
    background-color: var(--bg-bento) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-bento) !important;
    padding: 24px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}
[data-testid="metric-container"] label { color: var(--ink-muted) !important; font-size: 14px !important; }
[data-testid="metric-container"] div[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif !important; font-size: 36px !important; font-weight: 700 !important; color: var(--ink) !important; }

/* 2. Dataframes */
[data-testid="stDataFrame"] {
    background-color: var(--bg-bento) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border) !important;
    padding: 8px;
}

/* 3. Buttons */
.stButton > button {
    background-color: var(--bg-bento) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--ink) !important;
    font-weight: 500 !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.1);
}

/* 4. File Uploader */
[data-testid="stFileUploader"] > div > section {
    background-color: var(--bg-app) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 16px !important;
}
[data-testid="stFileUploader"] * { color: var(--ink) !important; }
[data-testid="stFileUploader"] button { background-color: var(--bg-bento) !important; border-radius: var(--radius-sm) !important; }

/* 5. Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-bento);
    border-right: 1px solid var(--border);
}

/* --- HEADER & NAVIGATION --- */
header { background-color: transparent !important; }
[data-testid="stHeaderActionElements"] { display: none; }

.sticky-header {
    position: fixed; top: 0; left: 0; width: 100%;
    background-color: rgba(9, 9, 11, 0.85); /* Matches --bg-app */
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    z-index: 99998; display: flex; justify-content: center; align-items: center;
    padding: 14px 0; padding-left: 60px; 
    border-bottom: 1px solid var(--border);
}
.sticky-title { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; margin: 0; color: var(--ink) !important; }
.emoji-icon { font-size: 28px; margin-right: 10px; }

.block-container { padding-top: 6rem !important; max-width: 1300px !important; }

/* --- CUSTOM BENTO HTML CLASSES --- */
.bento-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: auto auto;
    gap: 20px;
    margin-top: 20px;
}
.bento-card {
    background-color: var(--bg-bento);
    border: 1px solid var(--border);
    border-radius: var(--radius-bento);
    padding: 32px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.bento-hero { grid-column: span 2; grid-row: span 2; background: linear-gradient(145deg, var(--bg-bento), #111827); }
.bento-hero h1 { font-size: 48px; margin: 0 0 12px 0; line-height: 1.1; }
.bento-hero p { font-size: 18px; color: var(--ink-muted); margin: 0; }
.bento-small h3 { font-size: 20px; margin: 0 0 8px 0; }
.bento-small p { margin: 0; font-size: 14px; }
.bento-icon { font-size: 32px; margin-bottom: 16px; display: block; }

.pill { font-family: 'IBM Plex Mono', monospace; font-size: 11px; padding: 4px 12px; margin: 2px 4px 2px 0; border: 1px solid var(--border); border-radius: 999px; background: var(--bg-app); color: var(--ink-muted); display: inline-block;}
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center;">
        <span class="emoji-icon">🧠</span>
        <h1 class="sticky-title">InsightIQ</h1>
        <span style="margin-left:12px; font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--ink-muted); font-weight:400;">data refinery</span>
    </div>
</div>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

# ---------------------------------------------------------------------------
# 2. Core Logic Functions
# ---------------------------------------------------------------------------
def load_dataset(uploaded_file):
    name = uploaded_file.name.lower()
    uploaded_file.seek(0)
    try:
        if name.endswith(".csv"): return pd.read_csv(uploaded_file)
        elif name.endswith(".xlsx"): return pd.read_excel(uploaded_file, engine="openpyxl")
        elif name.endswith(".xls"): return pd.read_excel(uploaded_file, engine="xlrd")
        elif name.endswith(".jsonl"): return pd.read_json(uploaded_file, lines=True)
        elif name.endswith(".json"): return pd.read_json(uploaded_file)
        elif name.endswith(".xml"): return pd.read_xml(uploaded_file)
        elif name.endswith(".parquet"): return pd.read_parquet(uploaded_file)
        elif name.endswith(".avro"):
            try: import fastavro
            except ImportError:
                st.error("Reading .avro files needs the 'fastavro' package — install with: pip install fastavro")
                return None
            records = list(fastavro.reader(uploaded_file))
            return pd.DataFrame.from_records(records)
        else:
            st.warning(f"'{uploaded_file.name}' has an unsupported extension.")
            return None
    except Exception as e:
        st.error(f"Couldn't read '{uploaded_file.name}': {e}")
        return None

def commit_action(new_df):
    current_idx = st.session_state["history_index"]
    st.session_state["df_history"] = st.session_state["df_history"][:current_idx + 1]
    st.session_state["df_history"].append(new_df.copy())
    st.session_state["history_index"] += 1
    st.session_state["df"] = new_df.copy()

# ---------------------------------------------------------------------------
# 3. Sidebar — Command Center
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚡ Command Center")
    st.markdown("".join(f'<span class="pill">{fmt}</span>' for fmt in SUPPORTED_FORMATS), unsafe_allow_html=True)
    st.write("")

    uploaded_files = st.file_uploader("Upload data assets", type=SUPPORTED_FORMATS, accept_multiple_files=True)

    if uploaded_files:
        if "datasets" not in st.session_state: st.session_state["datasets"] = {}
        for f in uploaded_files:
            if f.name not in st.session_state["datasets"]:
                loaded = load_dataset(f)
                if loaded is not None: st.session_state["datasets"][f.name] = loaded

        if st.session_state.get("datasets"):
            active_name = st.selectbox("Active dataset", list(st.session_state["datasets"].keys()))
            
            if st.session_state.get("active_name") != active_name or "df_history" not in st.session_state:
                st.session_state["active_name"] = active_name
                initial_df = st.session_state["datasets"][active_name].copy()
                st.session_state["df_history"] = [initial_df]
                st.session_state["history_index"] = 0
                st.session_state["df"] = initial_df.copy()
                
            df_active = st.session_state["df"]
            st.markdown("---")
            st.markdown("### ⏳ Timeline")
            
            can_undo = st.session_state["history_index"] > 0
            can_redo = st.session_state["history_index"] < len(st.session_state["df_history"]) - 1
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⏪ Undo", disabled=not can_undo, use_container_width=True):
                    st.session_state["history_index"] -= 1
                    st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                    st.rerun()
            with c2:
                if st.button("⏩ Redo", disabled=not can_redo, use_container_width=True):
                    st.session_state["history_index"] += 1
                    st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                    st.rerun()
            st.caption(f"State: {st.session_state['history_index']} modifications")
    else:
        st.info("No data loaded yet. Upload above.")

# ---------------------------------------------------------------------------
# 4. Main Workspace (BENTO UI)
# ---------------------------------------------------------------------------
if "df" in st.session_state:
    df = st.session_state["df"]
    
    # BENTO ROW 1: Topline Metrics
    st.markdown("### 📊 Dataset Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows", f"{df.shape[0]:,}")
    m2.metric("Columns", df.shape[1])
    m3.metric("Duplicates", int(df.duplicated().sum()))
    m4.metric("Missing Data", f"{(df.isna().sum().sum() / df.size * 100) if df.size else 0:.1f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # BENTO ROW 2: Preview & Quick Actions
    col_data, col_actions = st.columns([2.5, 1])
    
    with col_data:
        st.markdown("### 🔍 Live Data Preview")
        st.dataframe(df.head(100), use_container_width=True, height=350)
        
    with col_actions:
        st.markdown("### 🧹 Quick Actions")
        with st.container(border=True):
            if st.button("🗑️ Drop Duplicate Rows", use_container_width=True):
                commit_action(df.drop_duplicates())
                st.rerun()
            if st.button("🚫 Drop Missing Values", use_container_width=True):
                commit_action(df.dropna())
                st.rerun()
            
            st.markdown("---")
            fill_strategy = st.selectbox("Fill strategy", ["mean", "median", "mode", "0"])
            if st.button("🩹 Fill Missing Values", use_container_width=True):
                df_filled = df.copy()
                for col in df_filled.columns:
                    if df_filled[col].isna().any():
                        if fill_strategy in ("mean", "median") and pd.api.types.is_numeric_dtype(df_filled[col]):
                            val = df_filled[col].mean() if fill_strategy == "mean" else df_filled[col].median()
                            df_filled[col] = df_filled[col].fillna(val)
                        elif fill_strategy == "mode":
                            mode_vals = df_filled[col].mode()
                            df_filled[col] = df_filled[col].fillna(mode_vals.iloc[0] if not mode_vals.empty else "")
                        elif fill_strategy == "0":
                            df_filled[col] = df_filled[col].fillna(0)
                commit_action(df_filled)
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # BENTO ROW 3: Visualization Explorer & Export
    col_viz, col_notes = st.columns([2, 1])
    
    with col_viz:
        st.markdown("### 📈 Visualization Engine")
        with st.container(border=True):
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            all_cols = df.columns.tolist()
            chart_theme = dict(plot_bgcolor="#18181B", paper_bgcolor="#18181B", font_family="IBM Plex Sans", font_color="#FAFAFA", margin=dict(t=30, b=30, l=30, r=30))

            v1, v2 = st.columns(2)
            with v1: chart_type = st.selectbox("Chart Type", ["Scatter Plot", "Bar Chart", "Line Chart", "Histogram"])
            with v2: x_axis = st.selectbox("Primary Axis (X)", all_cols)
            
            if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                y_axis = st.selectbox("Secondary Axis (Y)", numeric_cols)
                if chart_type == "Bar Chart": fig = px.bar(df, x=x_axis, y=y_axis, color_discrete_sequence=["#38BDF8"])
                elif chart_type == "Line Chart": fig = px.line(df, x=x_axis, y=y_axis, color_discrete_sequence=["#38BDF8"])
                elif chart_type == "Scatter Plot": fig = px.scatter(df, x=x_axis, y=y_axis, color_discrete_sequence=["#38BDF8"])
                
                fig.update_layout(**chart_theme)
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, color_discrete_sequence=["#38BDF8"])
                fig.update_layout(**chart_theme)
                st.plotly_chart(fig, use_container_width=True)

    with col_notes:
        st.markdown("### 📝 Insights & Export")
        if "analyst_notes" not in st.session_state: st.session_state["analyst_notes"] = ""
        st.session_state["analyst_notes"] = st.text_area("Observations:", value=st.session_state["analyst_notes"], height=180)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("⬇️ Export Clean CSV", df.to_csv(index=False).encode("utf-8"), file_name="refined_data.csv", mime="text/csv", use_container_width=True)
        
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine="openpyxl")
        st.download_button("⬇️ Export Excel", buffer.getvalue(), file_name="refined_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

else:
    # ---------------------------------------------------------------------------
    # EMPTY STATE: The Bento Grid Hero
    # ---------------------------------------------------------------------------
    st.markdown("""
    <div class="bento-grid">
        <div class="bento-card bento-hero">
            <h1>Refine your data<br>in real-time.</h1>
            <p>A powerful, completely client-side data studio. Upload your raw datasets and instantly start cleaning, transforming, and visualizing without writing a single line of code.</p>
        </div>
        <div class="bento-card bento-small">
            <span class="bento-icon">📥</span>
            <h3>Universal Import</h3>
            <p>Drop CSV, Excel, JSON, Parquet, or Avro files directly into the Command Center.</p>
        </div>
        <div class="bento-card bento-small">
            <span class="bento-icon">⚡</span>
            <h3>Time-Travel</h3>
            <p>Made a mistake? Use the built-in Undo/Redo timeline to revert any data transformation.</p>
        </div>
        <div class="bento-card bento-small" style="grid-column: span 2;">
            <span class="bento-icon">📊</span>
            <h3>Instant Visualization</h3>
            <p>Generate production-ready Plotly charts instantly. Spot trends, outliers, and insights in a beautiful dark-mode environment.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<p style="text-align:center;color:var(--ink-muted);font-family:\'IBM Plex Mono\',monospace;font-size:11px;margin-top:64px;">INSIGHTIQ · BENTO EDITION</p>', unsafe_allow_html=True)
