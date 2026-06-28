import io
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# 1. Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="InsightIQ | Data Refinery", page_icon="🧭", layout="wide")

# ---------------------------------------------------------------------------
# 2. Design tokens & Sticky Header
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --paper: #EEF3F7;
    --ink: #13315C;
    --teal: #1B6B72;
    --copper: #C77B2E;
    --slate: #5B6B79;
    --line: #C4D3DD;
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
    background-color: var(--paper);
    z-index: 99999;
    text-align: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--line);
    box-shadow: 0px 4px 12px rgba(19, 49, 92, 0.08);
}

.sticky-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: var(--ink);
    margin: 0;
    letter-spacing: 1px;
}

.stApp {
    background-color: var(--paper);
    background-image:
        linear-gradient(rgba(19,49,92,0.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(19,49,92,0.06) 1px, transparent 1px);
    background-size: 28px 28px;
}

/* Push content down so it doesn't hide behind the new sticky header */
.block-container { padding-top: 5.5rem; }

section[data-testid="stSidebar"] {
    background-color: #F7FAFB;
    border-right: 1px solid var(--line);
}

/* Type system */
.eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--copper); text-align: center; margin-bottom: 6px; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 58px; color: var(--ink); text-align: center; line-height: 1.05; margin: 4px 0 12px 0; }
.hero-sub { font-family: 'IBM Plex Sans', sans-serif; font-size: 19px; color: var(--slate); text-align: center; max-width: 620px; margin: 0 auto 14px auto; }
.status-strip { text-align: center; font-family: 'IBM Plex Mono', monospace; font-size: 12.5px; color: var(--teal); margin-bottom: 28px; }
.status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #2E9E5B; margin-right: 7px; box-shadow: 0 0 0 3px rgba(46,158,91,0.15); }

/* Section heading */
.section-eyebrow { font-family:'IBM Plex Mono',monospace; font-size:12px; letter-spacing:0.12em; text-transform:uppercase; color:var(--copper); margin-bottom:4px; }
.section-title { font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:26px; color:var(--ink); margin:0 0 6px 0; }

/* Pipeline flow animation */
.pipe-line { animation: flow 2.4s linear infinite; }
@keyframes flow { to { stroke-dashoffset: -28; } }
@media (prefers-reduced-motion: reduce) { .pipe-line { animation: none; } }

/* Stage captions */
.stage-eyebrow { font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:0.1em; color:var(--copper); text-transform:uppercase; }
.stage-title { font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:18px; color:var(--ink); margin:4px 0 6px 0; }
.stage-caption { font-family:'IBM Plex Sans',sans-serif; font-size:14px; color:var(--slate); line-height:1.5; }

/* Format pills in the sidebar */
.pill { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.04em; padding: 3px 10px; margin: 2px 4px 2px 0; border: 1px solid var(--teal); border-radius: 999px; color: var(--teal); background: rgba(27,107,114,0.06); }

/* Dashed section divider */
.dash-divider { border: none; border-top: 1px dashed var(--teal); margin: 30px 0; opacity: 0.6; }

/* Empty state */
.empty-state { border: 1px dashed var(--line); border-radius: 6px; padding: 56px 24px; text-align: center; background: rgba(255,255,255,0.5); }
.empty-state p { font-family:'IBM Plex Sans'; color:var(--slate); font-size:15px; margin-top:10px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--line); flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: 0.03em; color: var(--slate); padding: 10px 18px; }
.stTabs [aria-selected="true"] { color: var(--ink) !important; border-bottom: 2px solid var(--copper) !important; }

/* Buttons */
.stButton > button { font-family: 'IBM Plex Sans', sans-serif; border: 1px solid var(--ink); background-color: #FFFFFF; color: var(--ink); border-radius: 4px; font-weight: 500; transition: all 0.15s ease; }
.stButton > button:hover { background-color: var(--ink); color: #FFFFFF; border-color: var(--ink); }

footer, #MainMenu { visibility: hidden; }
</style>

<div class="sticky-header">
    <p class="sticky-title">🧠 InsightIQ</p>
</div>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

# ---------------------------------------------------------------------------
# 3. Hero
# ---------------------------------------------------------------------------
st.markdown('<p class="eyebrow">Data Operations Platform</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-title">InsightIQ</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Upload a dataset, clean it, reshape it, and chart it — all in one pass.</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="status-strip"><span class="status-dot"></span>'
    + f"{len(SUPPORTED_FORMATS)} formats supported &middot; "
    + " &middot; ".join(f.upper() for f in SUPPORTED_FORMATS)
    + "</p>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 4. Signature element — the data pipeline schematic
# ---------------------------------------------------------------------------
st.markdown('<p class="section-eyebrow" style="text-align:left;">The Process</p>', unsafe_allow_html=True)
st.markdown('<p class="section-title">How a dataset moves through InsightIQ</p>', unsafe_allow_html=True)

PIPELINE_SVG = """
<svg viewBox="0 0 1000 160" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;">
  <line x1="60" y1="80" x2="940" y2="80" stroke="#1B6B72" stroke-width="2" stroke-dasharray="8 6" class="pipe-line"/>
  <circle cx="180" cy="80" r="44" fill="#FFFFFF" stroke="#13315C" stroke-width="2"/>
  <g transform="translate(180,80)">
    <line x1="0" y1="-22" x2="0" y2="4" stroke="#13315C" stroke-width="3" stroke-linecap="round"/>
    <polyline points="-9,-4 0,5 9,-4" fill="none" stroke="#13315C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M -18,9 L -18,20 L 18,20 L 18,9" fill="none" stroke="#13315C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  </g>
  <circle cx="500" cy="80" r="44" fill="#FFFFFF" stroke="#13315C" stroke-width="2"/>
  <g transform="translate(500,80)">
    <path d="M -20,-18 L 20,-18 L 5,4 L 5,22 L -5,22 L -5,4 Z" fill="none" stroke="#13315C" stroke-width="3" stroke-linejoin="round"/>
  </g>
  <circle cx="820" cy="80" r="44" fill="#FFFFFF" stroke="#13315C" stroke-width="2"/>
  <g transform="translate(820,80)">
    <rect x="-20" y="2" width="10" height="18" fill="#13315C"/>
    <rect x="-5" y="-10" width="10" height="30" fill="#13315C"/>
    <rect x="10" y="-20" width="10" height="40" fill="#C77B2E"/>
  </g>
</svg>
"""
st.markdown(PIPELINE_SVG, unsafe_allow_html=True)

stage1, stage2, stage3 = st.columns(3)
with stage1:
    st.markdown('<p class="stage-eyebrow">Stage 01 · Acquire & Clean</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-title">Ingest & Purify</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-caption">Upload datasets from multiple formats, drop duplicates, and fix inconsistent entries.</p>', unsafe_allow_html=True)
with stage2:
    st.markdown('<p class="stage-eyebrow">Stage 02 · Process & Analyze</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-title">Shape & Explore</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-caption">Transform column structures and calculate deep statistical summaries automatically.</p>', unsafe_allow_html=True)
with stage3:
    st.markdown('<p class="stage-eyebrow">Stage 03 · Visualize & Decide</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-title">Find what matters</p>', unsafe_allow_html=True)
    st.markdown('<p class="stage-caption">Chart distributions and correlations to record insights and make final decisions.</p>', unsafe_allow_html=True)

st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 5. File loading
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

# ---------------------------------------------------------------------------
# 6. Sidebar — Command Center
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
            st.session_state["df"] = st.session_state["datasets"][active_name]
            st.session_state["active_name"] = active_name

            df_active = st.session_state["df"]
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Rows", f"{df_active.shape[0]:,}")
            c2.metric("Columns", df_active.shape[1])
    else:
        st.caption("No data loaded yet — upload a file above to begin.")

# ---------------------------------------------------------------------------
# 7. Main workspace (6 Tabs)
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
                st.session_state["df"] = df.drop_duplicates()
                st.rerun()
        with a2:
            if st.button("🚫 Drop rows with missing values"):
                st.session_state["df"] = df.dropna()
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
                st.session_state["df"] = df_filled
                st.rerun()
        st.markdown("#### Preview")
        st.dataframe(st.session_state["df"], use_container_width=True)

    # --- Tab 2: Data Processing --------------------------------------
    with tab2:
        st.markdown('<p class="stage-eyebrow">Stage 02</p>', unsafe_allow_html=True)
        st.markdown("### ⚙️ Data Processing")
        df = st.session_state["df"]
        t1, t2 = st.columns(2)
        with t1:
            cols_to_drop = st.multiselect("Drop columns", df.columns.tolist())
            if st.button("Drop selected") and cols_to_drop:
                st.session_state["df"] = df.drop(columns=cols_to_drop)
                st.rerun()
        with t2:
            col_to_rename = st.selectbox("Rename column", df.columns.tolist())
            new_name = st.text_input("New name")
            if st.button("Rename") and new_name:
                st.session_state["df"] = df.rename(columns={col_to_rename: new_name})
                st.rerun()
        st.markdown("#### Preview")
        st.dataframe(st.session_state["df"], use_container_width=True)

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
        chart_theme = dict(plot_bgcolor="#EEF3F7", paper_bgcolor="#EEF3F7", font_family="IBM Plex Sans")

        chart_type = st.selectbox(
            "Choose Visualization Type", 
            ["Dashboard View", "Scatter Plot", "Bar Chart", "Line Chart", "Area Chart", "Pie Chart", "Histogram", "Box Plot", "Correlation Heatmap"]
        )
        st.markdown("---")

        try:
            if chart_type == "Dashboard View":
                st.markdown("#### 🚀 Quick Insights Dashboard")
                if len(numeric_cols) >= 1 and len(all_cols) >= 2:
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        fig1 = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}", color_discrete_sequence=["#1B6B72"])
                        fig1.update_layout(**chart_theme)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        fig2 = px.pie(df, names=all_cols[0], title=f"Breakdown of {all_cols[0]}")
                        fig2.update_layout(**chart_theme)
                        st.plotly_chart(fig2, use_container_width=True)
                    with d_col2:
                        fig3 = px.box(df, y=numeric_cols[0], title=f"Spread of {numeric_cols[0]}", color_discrete_sequence=["#C77B2E"])
                        fig3.update_layout(**chart_theme)
                        st.plotly_chart(fig3, use_container_width=True)
                        
                        if len(numeric_cols) >= 2:
                            fig4 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}", color_discrete_sequence=["#13315C"])
                            fig4.update_layout(**chart_theme)
                            st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("Not enough numeric/categorical data to generate a dashboard.")

            elif chart_type in ["Bar Chart", "Line Chart", "Area Chart", "Scatter Plot"]:
                c1, c2, c3 = st.columns(3)
                with c1: x_axis = st.selectbox("X-Axis", all_cols)
                with c2: y_axis = st.selectbox("Y-Axis", numeric_cols)
                with c3: color_col = st.selectbox("Color by (Optional)", ["None"] + all_cols)
                
                color_param = None if color_col == "None" else color_col
                
                if chart_type == "Bar Chart": fig = px.bar(df, x=x_axis, y=y_axis, color=color_param)
                elif chart_type == "Line Chart": fig = px.line(df, x=x_axis, y=y_axis, color=color_param)
                elif chart_type == "Area Chart": fig = px.area(df, x=x_axis, y=y_axis, color=color_param)
                elif chart_type == "Scatter Plot": fig = px.scatter(df, x=x_axis, y=y_axis, color=color_param)
                
                fig.update_layout(**chart_theme)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Pie Chart":
                c1, c2 = st.columns(2)
                with c1: names = st.selectbox("Categories (Labels)", all_cols)
                with c2: values = st.selectbox("Values", numeric_cols)
                fig = px.pie(df, names=names, values=values)
                fig.update_layout(**chart_theme)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type in ["Histogram", "Box Plot"]:
                target_col = st.selectbox("Select Column to Analyze", numeric_cols)
                if chart_type == "Histogram": fig = px.histogram(df, x=target_col, color_discrete_sequence=["#1B6B72"])
                else: fig = px.box(df, y=target_col, color_discrete_sequence=["#C77B2E"])
                fig.update_layout(**chart_theme)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Correlation Heatmap":
                if len(numeric_cols) >= 2:
                    corr = df[numeric_cols].corr()
                    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=["#EEF3F7", "#1B6B72", "#13315C"])
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("You need at least two numeric columns to generate a correlation heatmap.")
                    
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
    st.markdown('<div class="empty-state"><p class="eyebrow">Awaiting input</p><p>No dataset loaded yet. Upload a file from the Command Center in the sidebar to begin.</p></div>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center;color:var(--slate);font-family:\'IBM Plex Mono\',monospace;font-size:11px;margin-top:40px;">DATA OPS / INSIGHTIQ — v1.4</p>', unsafe_allow_html=True)
