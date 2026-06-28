import io
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# 1. Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="InsightIQ | Data Refinery", page_icon="🧭", layout="wide")

# ---------------------------------------------------------------------------
# 1b. Sidebar visibility state (used by the custom slide toggle button)
# ---------------------------------------------------------------------------
if "sidebar_visible" not in st.session_state:
    st.session_state["sidebar_visible"] = True

# ---------------------------------------------------------------------------
# 2. Clean & Minimal Front Page Design
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;900&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --paper: #F8FAFC;
    --ink: #0F172A;
    --teal: #2563EB;
    --copper: #7C3AED;
    --slate: #475569;
    --line: #E2E8F0;
}

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

/* Hide Streamlit's default header */
header { visibility: hidden; }

/* Sticky Top Navigation Bar */
.sticky-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 99999;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 14px 0;
    border-bottom: 1px solid rgba(226, 232, 240, 0.8);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.sticky-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin: 0;
    color: var(--ink);
}

.emoji-icon {
    font-size: 28px;
    margin-right: 10px;
}

.stApp {
    background-color: var(--paper);
}

/* Push content down */
.block-container { 
    padding-top: 5rem !important;
    max-width: 1100px !important;
}

section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid var(--line);
}

/* Hero Section */
.hero-minimal {
    text-align: center;
    padding: 20px 0 8px 0;
}

.hero-minimal h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 42px;
    color: var(--ink);
    margin: 0 0 6px 0;
    letter-spacing: -1px;
}

.hero-minimal .subtitle {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 16px;
    color: var(--slate);
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Eyebrow label (small caps tag above a heading) */
.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--slate);
    margin: 0 0 6px 0;
}

/* "The Process" timeline section */
.process-section {
    text-align: center;
    max-width: 900px;
    margin: 28px auto 0 auto;
    padding: 0 20px;
}

.process-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 24px;
    color: var(--ink);
    margin: 0 0 28px 0;
    letter-spacing: -0.3px;
}

.timeline-row {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 640px;
    margin: 0 auto 24px auto;
    padding: 0 50px;
}

.timeline-line {
    position: absolute;
    top: 50%;
    left: 50px;
    right: 50px;
    border-top: 2px dashed var(--line);
    z-index: 0;
}

.timeline-icon {
    position: relative;
    z-index: 1;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 1.5px solid var(--ink);
    background: var(--paper);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
}

.stage-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 10px;
    text-align: left;
}

.stage-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--teal);
    margin: 0 0 6px 0;
}

.stage-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 16px;
    color: var(--ink);
    margin: 0 0 6px 0;
}

.stage-desc {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 13px;
    color: var(--slate);
    line-height: 1.5;
    margin: 0;
}

@media (max-width: 700px) {
    .stage-grid { grid-template-columns: 1fr; }
    .timeline-row { padding: 0 20px; }
}

/* Clean divider */
.dash-divider {
    border: none;
    border-top: 1px solid var(--line);
    margin: 16px 0 20px 0;
    opacity: 0.6;
}

/* Empty state */
.empty-state {
    border: 1px dashed var(--line);
    border-radius: 8px;
    padding: 48px 24px;
    text-align: center;
    background: #FFFFFF;
}

.empty-state h3 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--ink);
    margin: 0 0 4px 0;
}

.empty-state p {
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--slate);
    font-size: 14px;
    margin: 0;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { 
    gap: 2px; 
    border-bottom: 1px solid var(--line); 
    flex-wrap: wrap;
    background: transparent;
}
.stTabs [data-baseweb="tab"] { 
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.02em;
    color: var(--slate);
    padding: 8px 16px;
    border-radius: 6px 6px 0 0;
}
.stTabs [aria-selected="true"] { 
    color: var(--ink) !important; 
    border-bottom: 2px solid var(--teal) !important;
    font-weight: 600;
    background: transparent !important;
}

/* Buttons */
.stButton > button { 
    font-family: 'IBM Plex Sans', sans-serif;
    border: 1px solid var(--line);
    background-color: #FFFFFF;
    color: var(--ink);
    border-radius: 6px;
    font-weight: 500;
    font-size: 13px;
    transition: all 0.15s ease;
}
.stButton > button:hover { 
    background-color: var(--ink);
    color: #FFFFFF;
    border-color: var(--ink);
}

/* Metrics */
[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 12px;
    box-shadow: none;
}

footer, #MainMenu { visibility: hidden; }

/* Status dot */
.status-dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22C55E;
    margin-right: 6px;
}

.status-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--slate);
}

/* Pill tags */
.pill { 
    display: inline-block; 
    font-family: 'IBM Plex Mono', monospace; 
    font-size: 10px; 
    letter-spacing: 0.04em; 
    padding: 2px 10px; 
    margin: 2px 3px 2px 0; 
    border: 1px solid var(--line); 
    border-radius: 999px; 
    color: var(--slate); 
    background: #FFFFFF;
}

/* ----------------------------------------------------------------------- */
/* Custom sidebar slide toggle                                             */
/* The sticky header above sits at z-index 99999 and spans the full width, */
/* which was covering Streamlit's native sidebar collapse arrow — that's   */
/* why it looked "broken". We hide the native controls and drive the       */
/* sidebar with our own floating button + animated width instead.         */
/* ----------------------------------------------------------------------- */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

section[data-testid="stSidebar"] {
    transition: width 0.28s ease-in-out, min-width 0.28s ease-in-out, opacity 0.2s ease-in-out;
    overflow: hidden;
}

/* Floating toggle button — pinned top-left, above the sticky header */
.st-key-sb_toggle_btn {
    position: fixed;
    top: 9px;
    left: 18px;
    z-index: 100000;
}
.st-key-sb_toggle_btn button {
    width: 38px;
    height: 38px;
    padding: 0 !important;
    border-radius: 8px !important;
    font-size: 16px !important;
    line-height: 1 !important;
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center;">
        <span class="emoji-icon">🧠</span>
        <h1 class="sticky-title">InsightIQ</h1>
        <span style="margin-left:12px; font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--slate); font-weight:400;">data refinery</span>
    </div>
</div>
"""
, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 2b. Sidebar slide toggle — floating button + dynamic width/opacity CSS
# ---------------------------------------------------------------------------
_icon = "✕" if st.session_state["sidebar_visible"] else "☰"
_tip = "Hide sidebar" if st.session_state["sidebar_visible"] else "Show sidebar"
if st.button(_icon, key="sb_toggle_btn", help=_tip):
    st.session_state["sidebar_visible"] = not st.session_state["sidebar_visible"]
    st.rerun()

SIDEBAR_WIDTH = "21rem"
if st.session_state["sidebar_visible"]:
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{
            width: {SIDEBAR_WIDTH} !important;
            min-width: {SIDEBAR_WIDTH} !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"] {
            width: 0rem !important;
            min-width: 0rem !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

# ---------------------------------------------------------------------------
# 3. Hero Section
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-minimal">
    <p class="eyebrow" style="text-align:center;">Data Operations Platform</p>
    <h1>InsightIQ</h1>
    <p class="subtitle">Upload a dataset, clean it, reshape it, and chart it — all in one pass.</p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align:center; margin: 12px 0 8px 0;">
        <span class="status-dot"></span>
        <span class="status-text">{len(SUPPORTED_FORMATS)} formats supported · {" · ".join(f.upper() for f in SUPPORTED_FORMATS)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# --- "The Process" timeline -----------------------------------------------
st.markdown("""
<div class="process-section">
    <p class="eyebrow">The Process</p>
    <h2 class="process-title">How a dataset moves through InsightIQ</h2>
    <div class="timeline-row">
        <div class="timeline-line"></div>
        <div class="timeline-icon">📥</div>
        <div class="timeline-icon">⚙️</div>
        <div class="timeline-icon">📊</div>
    </div>
    <div class="stage-grid">
        <div class="stage-col">
            <p class="stage-tag">Stage 01 · Acquire &amp; Clean</p>
            <h3 class="stage-heading">Ingest &amp; Purify</h3>
            <p class="stage-desc">Upload datasets from multiple formats, drop duplicates, and fix inconsistent entries automatically.</p>
        </div>
        <div class="stage-col">
            <p class="stage-tag">Stage 02 · Process &amp; Analyze</p>
            <h3 class="stage-heading">Shape &amp; Explore</h3>
            <p class="stage-desc">Transform column structures and calculate deep statistical summaries automatically.</p>
        </div>
        <div class="stage-col">
            <p class="stage-tag">Stage 03 · Visualize &amp; Decide</p>
            <h3 class="stage-heading">Find what matters</h3>
            <p class="stage-desc">Chart distributions and correlations to record insights and make final decisions.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 4. Core Logic Functions
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
    """Saves a new dataframe state into the history timeline for Undo/Redo."""
    current_idx = st.session_state["history_index"]
    # If the user undid something and then made a new change, erase the alternate future timeline
    st.session_state["df_history"] = st.session_state["df_history"][:current_idx + 1]
    
    # Add the new change to the timeline
    st.session_state["df_history"].append(new_df.copy())
    st.session_state["history_index"] += 1
    st.session_state["df"] = new_df.copy()

# ---------------------------------------------------------------------------
# 5. Sidebar — Command Center (Now with Time Travel)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚡ Command Center")
    st.markdown("**Supported formats**")
    st.markdown("".join(f'<span class="pill">{fmt}</span>' for fmt in SUPPORTED_FORMATS), unsafe_allow_html=True)
    st.write("")

    uploaded_files = st.file_uploader("Upload your data assets", type=SUPPORTED_FORMATS, accept_multiple_files=True)

    if uploaded_files:
        if "datasets" not in st.session_state: st.session_state["datasets"] = {}
        for f in uploaded_files:
            if f.name not in st.session_state["datasets"]:
                loaded = load_dataset(f)
                if loaded is not None: st.session_state["datasets"][f.name] = loaded

        if st.session_state.get("datasets"):
            active_name = st.selectbox("Active dataset", list(st.session_state["datasets"].keys()))
            
            # If a new dataset is selected (or it's the first load), initialize the history timeline
            if st.session_state.get("active_name") != active_name or "df_history" not in st.session_state:
                st.session_state["active_name"] = active_name
                initial_df = st.session_state["datasets"][active_name].copy()
                st.session_state["df_history"] = [initial_df]
                st.session_state["history_index"] = 0
                st.session_state["df"] = initial_df.copy()

            df_active = st.session_state["df"]
            
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Rows", f"{df_active.shape[0]:,}")
            c2.metric("Columns", df_active.shape[1])
            
            # --- UNDO / REDO BUTTONS ---
            st.markdown("---")
            st.markdown("**⏳ Data Timeline**")
            u_col, r_col = st.columns(2)
            
            can_undo = st.session_state["history_index"] > 0
            can_redo = st.session_state["history_index"] < len(st.session_state["df_history"]) - 1
            
            if u_col.button("⏪ Undo", disabled=not can_undo, use_container_width=True):
                st.session_state["history_index"] -= 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()
                
            if r_col.button("⏩ Redo", disabled=not can_redo, use_container_width=True):
                st.session_state["history_index"] += 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()
    else:
        st.caption("No data loaded yet — upload a file above to begin.")

# ---------------------------------------------------------------------------
# 6. Main workspace
# ---------------------------------------------------------------------------
if "df" in st.session_state:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧹 Data Cleaning", "⚙️ Data Processing", "📊 Data Analysis", 
        "📈 Data Visualize", "💡 Interpretation", "🎯 Decision Making"
    ])

    # --- Tab 1: Data Cleaning -----------------------------------------
    with tab1:
        st.markdown('<p class="stage-eyebrow">Stage 01</p>', unsafe_allow_html=True)
        st.markdown("### 🧹 Data Cleaning")
        df = st.session_state["df"]

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Missing values by column**")
            missing = df.isna().sum()
            missing = missing[missing > 0]
            if missing.empty: st.success("No missing values detected.")
            else: st.dataframe(missing.rename("missing count"), use_container_width=True)
        with colB:
            st.markdown("**Duplicate rows**")
            st.metric("Duplicates found", int(df.duplicated().sum()))

        st.markdown("#### Actions")
        a1, a2, a3 = st.columns(3)
        with a1:
            if st.button("🗑️ Drop duplicate rows"):
                commit_action(df.drop_duplicates())
                st.rerun()
        with a2:
            if st.button("🚫 Drop rows with missing values"):
                commit_action(df.dropna())
                st.rerun()
        with a3:
            fill_strategy = st.selectbox("Fill missing with", ["mean", "median", "mode", "0"])
            if st.button("🩹 Fill missing values"):
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
        st.markdown("#### Data Preview")
        st.dataframe(st.session_state["df"].head(100), use_container_width=True)

    # --- Tab 2: Data Processing --------------------------------------
    with tab2:
        st.markdown('<p class="stage-eyebrow">Stage 02</p>', unsafe_allow_html=True)
        st.markdown("### ⚙️ Data Processing")
        df = st.session_state["df"]
        t1, t2 = st.columns(2)
        with t1:
            cols_to_drop = st.multiselect("Drop columns", df.columns.tolist())
            if st.button("Drop selected") and cols_to_drop:
                commit_action(df.drop(columns=cols_to_drop))
                st.rerun()
        with t2:
            col_to_rename = st.selectbox("Rename column", df.columns.tolist())
            new_name = st.text_input("New name")
            if st.button("Rename") and new_name:
                commit_action(df.rename(columns={col_to_rename: new_name}))
                st.rerun()
        st.markdown("#### Data Preview")
        st.dataframe(st.session_state["df"].head(100), use_container_width=True)

    # --- Tab 3: Data Analysis ----------------------------------------
    with tab3:
        st.markdown('<p class="stage-eyebrow">Stage 03</p>', unsafe_allow_html=True)
        st.markdown("### 📊 Data Analysis")
        df = st.session_state["df"]
        st.markdown("#### Summary Statistics")
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    # --- Tab 4: Data Visualize --------------
    with tab4:
        st.markdown('<p class="stage-eyebrow">Stage 04</p>', unsafe_allow_html=True)
        st.markdown("### 📈 Data Visualize")
        
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        chart_theme = dict(plot_bgcolor="#F8FAFC", paper_bgcolor="#F8FAFC", font_family="IBM Plex Sans", margin=dict(t=40, b=40, l=40, r=40))

        chart_type = st.selectbox(
            "Choose Visualization Type", 
            ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Dashboard View"]
        )
        st.markdown("---")

        try:
            if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                # 1. Controls
                c1, c2, c3 = st.columns(3)
                with c1: x_axis = st.selectbox("X-Axis", all_cols)
                with c2: y_axis = st.selectbox("Y-Axis", numeric_cols)
                with c3: color_col = st.selectbox("Color by (Optional)", ["None"] + all_cols)
                
                color_param = None if color_col == "None" else color_col
                
                # 2. Split screen: 75% for Chart, 25% for Side Data
                chart_col, data_col = st.columns([3, 1])
                
                with chart_col:
                    if chart_type == "Bar Chart": 
                        fig = px.bar(df, x=x_axis, y=y_axis, color=color_param, text_auto='.2s')
                        fig.update_traces(textposition="outside", cliponaxis=False)
                    elif chart_type == "Line Chart": 
                        fig = px.line(df, x=x_axis, y=y_axis, color=color_param, markers=True)
                    elif chart_type == "Scatter Plot": 
                        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_param)
                    
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)
                
                with data_col:
                    st.markdown("#### 📝 Data Summary")
                    st.caption(f"Analyzing **{y_axis}** by **{x_axis}**")
                    st.write("**Top 5 Highest Values:**")
                    top_data = df[[x_axis, y_axis]].sort_values(by=y_axis, ascending=False).head(5)
                    st.dataframe(top_data, hide_index=True, use_container_width=True)

            elif chart_type == "Pie Chart":
                c1, c2 = st.columns(2)
                with c1: names = st.selectbox("Categories (Labels)", all_cols)
                with c2: values = st.selectbox("Values", numeric_cols)
                
                chart_col, data_col = st.columns([3, 1])
                
                with chart_col:
                    fig = px.pie(df, names=names, values=values)
                    fig.update_traces(textinfo='label+percent+value', textposition='inside')
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)
                    
                with data_col:
                    st.markdown("#### 📝 Data Summary")
                    st.write("**Category Breakdown:**")
                    pie_data = df.groupby(names)[values].sum().reset_index().sort_values(by=values, ascending=False)
                    st.dataframe(pie_data, hide_index=True, use_container_width=True)

            elif chart_type == "Dashboard View":
                st.markdown("#### 🚀 Quick Insights Dashboard")
                if len(numeric_cols) >= 1 and len(all_cols) >= 2:
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        fig1 = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}", text_auto=True, color_discrete_sequence=["#2563EB"])
                        fig1.update_layout(**chart_theme)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        fig2 = px.pie(df, names=all_cols[0], title=f"Breakdown of {all_cols[0]}")
                        fig2.update_traces(textinfo='percent+label')
                        fig2.update_layout(**chart_theme)
                        st.plotly_chart(fig2, use_container_width=True)
                    with d_col2:
                        fig3 = px.box(df, y=numeric_cols[0], title=f"Spread of {numeric_cols[0]}", color_discrete_sequence=["#7C3AED"])
                        fig3.update_layout(**chart_theme)
                        st.plotly_chart(fig3, use_container_width=True)
                        
                        if len(numeric_cols) >= 2:
                            fig4 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}", color_discrete_sequence=["#0F172A"])
                            fig4.update_layout(**chart_theme)
                            st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("Not enough numeric/categorical data to generate a dashboard.")
                    
            elif chart_type == "Histogram":
                target_col = st.selectbox("Select Column to Analyze", numeric_cols)
                chart_col, data_col = st.columns([3, 1])
                
                with chart_col:
                    fig = px.histogram(df, x=target_col, text_auto=True, color_discrete_sequence=["#2563EB"])
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)
                with data_col:
                    st.markdown("#### 📝 Statistics")
                    st.metric("Average (Mean)", f"{df[target_col].mean():.2f}")
                    st.metric("Median", f"{df[target_col].median():.2f}")
                    st.metric("Max Value", f"{df[target_col].max():.2f}")

        except Exception as e:
            st.error(f"Could not generate {chart_type}. Please ensure your data types are compatible. Error: {e}")

    # --- Tab 5: Interpretation ---------------------------------------------
    with tab5:
        st.markdown('<p class="stage-eyebrow">Stage 05</p>', unsafe_allow_html=True)
        st.markdown("### 💡 Interpretation")
        if "analyst_notes" not in st.session_state: st.session_state["analyst_notes"] = ""
        st.session_state["analyst_notes"] = st.text_area("Observations:", value=st.session_state["analyst_notes"], height=300)

    # --- Tab 6: Decision Making ---------------------------------------------
    with tab6:
        st.markdown('<p class="stage-eyebrow">Stage 06</p>', unsafe_allow_html=True)
        st.markdown("### 🎯 Decision Making")
        df = st.session_state["df"]
        m1, m2, m3 = st.columns(3)
        m1.metric("Final Total Rows", f"{df.shape[0]:,}")
        m2.metric("Final Total Columns", df.shape[1])
        m3.metric("Remaining Missing Data", f"{(df.isna().sum().sum() / df.size * 100) if df.size else 0:.1f}%")

        st.markdown("#### Final Export")
        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button("⬇️ Download CSV", df.to_csv(index=False).encode("utf-8"), file_name="insightiq_export.csv", mime="text/csv", use_container_width=True)
        with e2:
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button("⬇️ Download Excel", buffer.getvalue(), file_name="insightiq_export.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with e3:
            final_notes = st.session_state.get("analyst_notes", "No notes recorded.")
            st.download_button("⬇️ Download Notes", final_notes.encode("utf-8"), file_name="analyst_notes.txt", mime="text/plain", use_container_width=True)

else:
    st.markdown("""
    <div class="empty-state">
        <h3>📂 No dataset loaded</h3>
        <p>Upload a file from the Command Center in the sidebar to begin.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<p style="text-align:center;color:var(--slate);font-family:\'IBM Plex Mono\',monospace;font-size:11px;margin-top:32px;">INSIGHTIQ · data refinery</p>', unsafe_allow_html=True)
