import os

os.makedirs(".github/workflows", exist_ok=True)

app_code = r'''import io
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="InsightIQ | Data Refinery", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-main: #F8FAFC;
    --text-dark: #0F172A;
    --text-muted: #64748B;
    --accent-1: #3B82F6; 
    --accent-2: #8B5CF6; 
    --border-light: #E2E8F0;
    --card-bg: rgba(255, 255, 255, 0.85);
}

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp { 
    background-color: var(--bg-main);
    background-image: radial-gradient(#CBD5E1 1px, transparent 1px);
    background-size: 24px 24px;
}

header[data-testid="stHeader"] { 
    background: transparent !important;
    z-index: 99999 !important;
}

[data-testid="stHeaderActionElements"] { display: none; }

[data-testid="collapsedControl"] {
    z-index: 100000 !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

.block-container { padding-top: 6rem !important; max-width: 1200px !important; }

.sticky-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 64px;
    background: rgba(248, 250, 252, 0.9);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    z-index: 99990;
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid rgba(226, 232, 240, 0.6);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}

.sticky-title {
    font-family: 'Outfit', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-minimal { text-align: center; padding: 20px 15px 15px 15px; }
.hero-minimal h1 { font-weight: 800; font-size: 48px; color: var(--text-dark); margin: 0 0 10px 0; letter-spacing: -1.5px; line-height: 1.1; }
.hero-minimal .subtitle { font-size: 18px; color: var(--text-muted); max-width: 600px; margin: 0 auto; }

.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; margin: 20px auto 0 auto; padding: 0 20px; }
.feature-item { background: var(--card-bg); backdrop-filter: blur(10px); border: 1px solid var(--border-light); border-radius: 16px; padding: 24px 16px; text-align: center; transition: transform 0.2s ease, box-shadow 0.2s ease; }
.feature-item:hover { transform: translateY(-4px); box-shadow: 0 12px 24px -8px rgba(59, 130, 246, 0.15); border-color: rgba(59, 130, 246, 0.3); }
.feature-item .icon { font-size: 32px; display: block; margin-bottom: 8px; }
.feature-item .label { font-size: 16px; font-weight: 700; color: var(--text-dark); }
.feature-item .desc { font-size: 13px; color: var(--text-muted); margin: 0; }

.empty-state { border: 2px dashed var(--border-light); border-radius: 16px; padding: 60px 24px; text-align: center; background: var(--card-bg); backdrop-filter: blur(10px); }
.empty-state h3 { font-size: 20px; font-weight: 700; color: var(--text-dark); margin: 0 0 8px 0; }

.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid var(--border-light); background: transparent; }
.stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text-muted); padding: 12px 16px; }
.stTabs [aria-selected="true"] { color: var(--accent-1) !important; border-bottom: 3px solid var(--accent-1) !important; font-weight: 700; }

.stButton > button { font-family: 'Outfit', sans-serif; font-weight: 600; border-radius: 8px; transition: all 0.2s ease; width: 100%; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--accent-1), var(--accent-2)); border: none; }

[data-testid="metric-container"] { background: var(--card-bg); border: 1px solid var(--border-light); border-radius: 12px; padding: 16px; backdrop-filter: blur(10px); }

.pill { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 4px 12px; margin: 4px; border-radius: 999px; background: rgba(59, 130, 246, 0.1); color: var(--accent-1); font-weight: 600; }

@media (max-width: 768px) {
    .block-container { padding-top: 5rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    
    .sticky-header { 
        width: calc(100% - 50px) !important;
        margin-left: 50px !important;
        justify-content: flex-start; 
        padding-left: 15px; 
    }
    
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 12px !important;
    }

    .sticky-title { font-size: 22px !important; }
    .hero-minimal { padding-top: 10px; }
    .hero-minimal h1 { font-size: 32px; line-height: 1.2; }
    .hero-minimal .subtitle { font-size: 15px; }
    .feature-grid { grid-template-columns: 1fr; gap: 12px; padding: 0; }
    .feature-item { padding: 16px 12px; display: flex; align-items: center; text-align: left; }
    .feature-item .icon { font-size: 28px; margin-right: 15px; margin-bottom: 0; }
    
    .stTabs [data-baseweb="tab-list"] { flex-wrap: nowrap; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; padding-bottom: 5px; }
    .stTabs [data-baseweb="tab"] { font-size: 11px; padding: 8px 12px; white-space: nowrap; }
    [data-testid="metric-container"] { margin-bottom: 10px; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
}
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center;">
        <span style="font-size: 24px; margin-right: 8px;">🌌</span>
        <h1 class="sticky-title">InsightIQ</h1>
    </div>
</div>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

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
            try: 
                import fastavro
            except ImportError:
                st.error("Install 'fastavro' package: pip install fastavro")
                return None
            records = list(fastavro.reader(uploaded_file))
            return pd.DataFrame.from_records(records)
        else:
            return None
    except:
        return None

def commit_action(new_df):
    current_idx = st.session_state["history_index"]
    st.session_state["df_history"] = st.session_state["df_history"][:current_idx + 1]
    st.session_state["df_history"].append(new_df.copy())
    st.session_state["history_index"] += 1
    st.session_state["df"] = new_df.copy()

with st.sidebar:
    st.markdown("### ⚙️ Engine Control")
    st.markdown("".join(f'<span class="pill">{fmt}</span>' for fmt in SUPPORTED_FORMATS), unsafe_allow_html=True)
    st.write("")
    uploaded_files = st.file_uploader("Drop datasets here", type=SUPPORTED_FORMATS, accept_multiple_files=True)

    if not uploaded_files:
        for key in ["datasets", "active_name", "df", "df_history", "history_index", "pivot_results"]:
            if key in st.session_state:
                del st.session_state[key]
        st.caption("Awaiting data ingestion...")
    else:
        current_files = {f.name: f for f in uploaded_files}
        
        if "datasets" in st.session_state:
            st.session_state["datasets"] = {k: v for k, v in st.session_state["datasets"].items() if k in current_files}
        else:
            st.session_state["datasets"] = {}
            
        for fname, fobj in current_files.items():
            if fname not in st.session_state["datasets"]:
                loaded = load_dataset(fobj)
                if loaded is not None:
                    st.session_state["datasets"][fname] = loaded

        if st.session_state["datasets"]:
            active_name = st.selectbox("Active Pipeline", list(st.session_state["datasets"].keys()))
            if st.session_state.get("active_name") != active_name or "df_history" not in st.session_state:
                st.session_state["active_name"] = active_name
                initial_df = st.session_state["datasets"][active_name].copy()
                st.session_state["df_history"] = [initial_df]
                st.session_state["history_index"] = 0
                st.session_state["df"] = initial_df.copy()
                st.session_state["pivot_results"] = []
            
            df_active = st.session_state["df"]
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Rows", f"{df_active.shape[0]:,}")
            c2.metric("Columns", df_active.shape[1])
        else:
            for key in ["active_name", "df", "df_history", "history_index", "pivot_results"]:
                if key in st.session_state:
                    del st.session_state[key]

if "df" in st.session_state:
    with st.container(border=True):
        col_info, col_undo, col_redo = st.columns([6, 2, 2])
        can_undo = st.session_state["history_index"] > 0
        can_redo = st.session_state["history_index"] < len(st.session_state["df_history"]) - 1
        with col_info:
            st.markdown(f"**Pipeline:** `{st.session_state['active_name']}` | **Transformations:** `{st.session_state['history_index']}`")
        with col_undo:
            if st.button("⏪ Undo", disabled=not can_undo, use_container_width=True):
                st.session_state["history_index"] -= 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()
        with col_redo:
            if st.button("⏩ Redo", disabled=not can_redo, use_container_width=True):
                st.session_state["history_index"] += 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()

    with st.expander("👁️ View Live Dataset Preview", expanded=False):
        st.dataframe(st.session_state["df"].head(100), use_container_width=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧬 Data Cleaning", 
        "⚙️ Transform", 
        "🔀 Pivot Analysis", 
        "📈 Dashboard", 
        "💾 Export",
        "📊 Matrix Dashboard"
    ])

    with tab1:
        df = st.session_state["df"]
        with st.container(border=True):
            st.markdown("#### Anomaly Detection")
            colA, colB = st.columns(2)
            with colA:
                missing = df.isna().sum()
                missing = missing[missing > 0]
                if missing.empty: 
                    st.success("✓ Zero missing values detected.")
                else: 
                    st.dataframe(missing.rename("Missing Count"), use_container_width=True)
            with colB:
                dupes = int(df.duplicated().sum())
                if dupes == 0:
                    st.success("✓ Zero duplicate rows detected.")
                else:
                    st.warning(f"⚠️ {dupes} duplicate rows detected.")

        with st.container(border=True):
            st.markdown("#### Resolution Actions")
            a1, a2, a3 = st.columns([1, 1, 2])
            with a1:
                if st.button("🗑️ Drop Duplicates", use_container_width=True):
                    commit_action(df.drop_duplicates())
                    st.rerun()
            with a2:
                if st.button("🚫 Drop Missing", use_container_width=True):
                    commit_action(df.dropna())
                    st.rerun()
            with a3:
                fill_col1, fill_col2 = st.columns([1, 1])
                with fill_col1:
                    fill_strategy = st.selectbox("Imputation Method", ["mean", "median", "mode", "0"], label_visibility="collapsed")
                with fill_col2:
                    if st.button("🩹 Impute Values", use_container_width=True):
                        df_filled = df.copy()
                        cleaner_map = {"nane": np.nan, "null": np.nan, "NaN": np.nan, "nan": np.nan, "NA": np.nan}
                        df_filled = df_filled.replace(cleaner_map)
                        
                        for col in df_filled.columns:
                            if df_filled[col].dtype == 'object':
                                try:
                                    df_filled[col] = pd.to_numeric(df_filled[col])
                                except:
                                    pass
                                    
                        for col in df_filled.columns:
                            if df_filled[col].isna().any():
                                if fill_strategy in ("mean", "median"):
                                    if pd.api.types.is_numeric_dtype(df_filled[col]):
                                        val = df_filled[col].mean() if fill_strategy == "mean" else df_filled[col].median()
                                        df_filled[col] = df_filled[col].fillna(val)
                                    else:
                                        mode_vals = df_filled[col].mode()
                                        val = mode_vals.iloc[0] if not mode_vals.empty else "Unknown"
                                        df_filled[col] = df_filled[col].fillna(val)
                                elif fill_strategy == "mode":
                                    mode_vals = df_filled[col].mode()
                                    val = mode_vals.iloc[0] if not mode_vals.empty else "Unknown"
                                    df_filled[col] = df_filled[col].fillna(val)
                                elif fill_strategy == "0":
                                    if pd.api.types.is_numeric_dtype(df_filled[col]):
                                        df_filled[col] = df_filled[col].fillna(0)
                                    else:
                                        df_filled[col] = df_filled[col].fillna("0")
                        commit_action(df_filled)
                        st.rerun()

    with tab2:
        df = st.session_state["df"]
        with st.container(border=True):
            t1, t2 = st.columns(2)
            with t1:
                st.markdown("#### Drop Dimensions")
                cols_to_drop = st.multiselect("Select columns to remove", df.columns.tolist(), label_visibility="collapsed")
                if st.button("Execute Drop", use_container_width=True) and cols_to_drop:
                    commit_action(df.drop(columns=cols_to_drop))
                    st.rerun()
            with t2:
                st.markdown("#### Rename Dimensions")
                col_to_rename = st.selectbox("Target column", df.columns.tolist(), label_visibility="collapsed")
                new_name = st.text_input("New name", placeholder="New name...", label_visibility="collapsed")
                if st.button("Execute Rename", use_container_width=True) and new_name:
                    commit_action(df.rename(columns={col_to_rename: new_name}))
                    st.rerun()

    with tab3:
        df = st.session_state["df"]
        if "pivot_results" not in st.session_state: st.session_state["pivot_results"] = []
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        
        with st.expander("➕ Generate Matrix", expanded=True if not st.session_state["pivot_results"] else False):
            with st.form("pivot_form"):
                p_col1, p_col2, p_col3 = st.columns(3)
                with p_col1: pivot_index = st.selectbox("Index (Rows)", ["None"] + all_cols)
                with p_col2: pivot_values = st.selectbox("Target Value", ["None"] + numeric_cols)
                with p_col3: pivot_agg = st.selectbox("Aggregation", ["mean", "sum", "count", "max", "min"])
                pivot_name = st.text_input("Matrix Identifier", value=f"Analysis Matrix {len(st.session_state['pivot_results']) + 1}")
                create_pivot = st.form_submit_button("Generate Matrix", type="primary", use_container_width=True)

            if create_pivot and pivot_index != "None" and pivot_values != "None":
                try:
                    agg_col_name = f"{pivot_values}_{pivot_agg}"
                    pivot_series = df.groupby(pivot_index)[pivot_values].agg(pivot_agg)
                    pivot_df = pivot_series.reset_index(name=agg_col_name)
                    
                    st.session_state["pivot_results"].append({
                        "name": pivot_name, 
                        "df": pivot_df, 
                        "index": pivot_index, 
                        "value": agg_col_name,
                        "original_value": pivot_values, 
                        "agg": pivot_agg
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating matrix: {str(e)}")
        
        if st.session_state["pivot_results"]:
            st.markdown("### Computed Matrices")
            pivot_names = [p["name"] for p in st.session_state["pivot_results"]]
            
            seen = {}
            unique_names = []
            for name in pivot_names:
                if name in seen:
                    seen[name] += 1
                    unique_names.append(f"{name} ({seen[name]})")
                else:
                    seen[name] = 0
                    unique_names.append(name)
                    
            pivot_tabs = st.tabs(unique_names)
            for i, tab in enumerate(pivot_tabs):
                with tab:
                    p_data = st.session_state["pivot_results"][i]
                    pdf = p_data["df"]
                    with st.container(border=True):
                        val_label = p_data.get("original_value", p_data["value"])
                        st.caption(f"**{p_data['agg'].upper()}** of **{val_label}** by **{p_data['index']}**")
                        st.dataframe(pdf, use_container_width=True)
                        try:
                            fig = px.bar(pdf, x=p_data["index"], y=p_data["value"], color=p_data["value"], color_continuous_scale="Blues")
                            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, b=20, l=0, r=0))
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as plot_err: 
                            st.warning(f"Could not render chart: {plot_err}")
                            
                        if st.button(f"🗑️ Delete Matrix", key=f"del_{i}", use_container_width=True):
                            st.session_state["pivot_results"].pop(i)
                            st.rerun()

    with tab4:
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        chart_theme = dict(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_family="Outfit", margin=dict(t=40, b=40, l=0, r=0))

        with st.container(border=True):
            chart_type = st.selectbox("Visualization Engine", ["Automated Dashboard", "Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram"])
            try:
                if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:
                    c1, c2, c3 = st.columns(3)
                    with c1: x_axis = st.selectbox("X-Axis (Dimension)", all_cols)
                    with c2: y_axis = st.selectbox("Y-Axis (Measure)", numeric_cols)
                    with c3: color_col = st.selectbox("Color Segment", ["None"] + all_cols)
                    
                    color_param = None if color_col == "None" else color_col
                    
                    if chart_type == "Bar Chart": fig = px.bar(df, x=x_axis, y=y_axis, color=color_param)
                    elif chart_type == "Line Chart": fig = px.line(df, x=x_axis, y=y_axis, color=color_param, markers=True)
                    elif chart_type == "Scatter Plot": fig = px.scatter(df, x=x_axis, y=y_axis, color=color_param)
                    
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Pie Chart":
                    c1, c2 = st.columns(2)
                    with c1: names = st.selectbox("Categories", all_cols)
                    with c2: values = st.selectbox("Values", numeric_cols)
                    fig = px.pie(df, names=names, values=values, hole=0.4)
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Automated Dashboard":
                    if len(numeric_cols) >= 1 and len(all_cols) >= 2:
                        d_col1, d_col2 = st.columns(2)
                        with d_col1:
                            fig1 = px.histogram(df, x=numeric_cols[0], title=f"Density: {numeric_cols[0]}", color_discrete_sequence=["#3B82F6"])
                            fig1.update_layout(**chart_theme)
                            st.plotly_chart(fig1, use_container_width=True)
                            fig2 = px.pie(df, names=all_cols[0], title=f"Segments: {all_cols[0]}", hole=0.3)
                            fig2.update_layout(**chart_theme)
                            st.plotly_chart(fig2, use_container_width=True)
                        with d_col2:
                            fig3 = px.box(df, y=numeric_cols[0], title=f"Variance: {numeric_cols[0]}", color_discrete_sequence=["#8B5CF6"])
                            fig3.update_layout(**chart_theme)
                            st.plotly_chart(fig3, use_container_width=True)
                            if len(numeric_cols) >= 2:
                                fig4 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"Correlation: {numeric_cols[0]} v {numeric_cols[1]}")
                                fig4.update_layout(**chart_theme)
                                st.plotly_chart(fig4, use_container_width=True)

                elif chart_type == "Histogram":
                    target_col = st.selectbox("Target Metric", numeric_cols)
                    fig = px.histogram(df, x=target_col, color_discrete_sequence=["#3B82F6"])
                    fig.update_layout(**chart_theme)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("#### Metric Summary")
                    h_col1, h_col2, h_col3 = st.columns(3)
                    h_col1.metric("Mean Average", f"{df[target_col].mean():.2f}")
                    h_col2.metric("Median Value", f"{df[target_col].median():.2f}")
                    h_col3.metric("Maximum Value", f"{df[target_col].max():.2f}")
            except:
                pass

    with tab5:
        df = st.session_state["df"]
        with st.container(border=True):
            st.markdown("### Export Final Payload")
            m1, m2 = st.columns(2)
            m1.metric("Total Matrix Rows", f"{df.shape[0]:,}")
            m2.metric("Total Matrix Columns", df.shape[1])
            st.write("")
            e1, e2 = st.columns(2)
            with e1:
                st.download_button("Download CSV File", df.to_csv(index=False).encode("utf-8"), file_name="insightiq_payload.csv", mime="text/csv", use_container_width=True)
            with e2:
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine="openpyxl")
                st.download_button("Download Excel File", buffer.getvalue(), file_name="insightiq_payload.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

    with tab6:
        st.markdown("### 📊 Consolidated Matrix Dashboard")
        if "pivot_results" in st.session_state and st.session_state["pivot_results"]:
            matrices = st.session_state["pivot_results"]
            
            for i in range(0, len(matrices), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(matrices):
                        p_data = matrices[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                val_label = p_data.get("original_value", p_data["value"])
                                st.markdown(f"#### {p_data['name']}")
                                st.caption(f"**{p_data['agg'].upper()}** of **{val_label}** by **{p_data['index']}**")
                                
                                try:
                                    fig = px.bar(p_data["df"], x=p_data["index"], y=p_data["value"], color=p_data["value"], color_continuous_scale="Blues")
                                    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, b=10, l=0, r=0), height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                                except: 
                                    st.warning("Chart render failed.")
                                
                                with st.expander("👁️ View Data Matrix"):
                                    st.dataframe(p_data["df"], use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### Export Comprehensive Report")
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state["df"].to_excel(writer, sheet_name="Master Data", index=False)
                for p_data in st.session_state["pivot_results"]:
                    sheet_name = p_data["name"][:31].replace(":", "").replace("/", "")
                    p_data["df"].to_excel(writer, sheet_name=sheet_name, index=False)
            
            st.download_button(
                "📥 Download Complete Report (Excel)", 
                buffer.getvalue(), 
                file_name="InsightIQ_Complete_Report.xlsx", 
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
        else:
            st.info("No matrices generated yet. Go to '🔀 Pivot Analysis' to create some.")

else:
    st.markdown("""
    <div class="hero-minimal">
        <h1>Data Refinery, Reimagined.</h1>
        <p class="subtitle">Upload raw datasets and extract visual insights instantly on any device.</p>
    </div>
    <div class="feature-grid">
        <div class="feature-item">
            <span class="icon">⚡</span>
            <div>
                <div class="label">Universal Import</div>
                <p class="desc">Supports 8 data formats</p>
            </div>
        </div>
        <div class="feature-item">
            <span class="icon">🧬</span>
            <div>
                <div class="label">Smart Cleaning</div>
                <p class="desc">Handle anomalies instantly</p>
            </div>
        </div>
        <div class="feature-item">
            <span class="icon">🔮</span>
            <div>
                <div class="label">Visual Analytics</div>
                <p class="desc">Interactive dashboard views</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div style="text-align:center; margin: 20px 0;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #3B82F6; margin-right: 8px; box-shadow: 0 0 8px #3B82F6;"></span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-muted); font-weight: 500;">Engine Online · {len(SUPPORTED_FORMATS)} Formats Supported</span>
        </div>
        <hr style="border:none; border-top: 1px solid var(--border-light); margin-bottom: 30px;">
        """,
        unsafe_allow_html=True,
    )
'''

bot_code = r'''import os
from playwright.sync_api import sync_playwright, TimeoutError

TARGET_URL = os.getenv("APP_URL", "https://your-app-name.streamlit.app/")

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    
    try:
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(15000) 
    except TimeoutError:
        pass
    except Exception:
        pass
    finally:
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
'''

req_code = r'''streamlit
pandas
plotly
openpyxl
fastavro
xlrd
playwright
'''

yaml_code = r'''name: Keep Streamlit Awake

on:
  schedule:
    - cron: '0 */10 * * *'
  workflow_dispatch: 

jobs:
  ping-app:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          
      - name: Install Playwright & OS Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install playwright
          playwright install chromium
          sudo npx playwright install-deps chromium
          
      - name: Run the bot
        env:
          APP_URL: "https://your-app-name.streamlit.app/" 
        run: python keep_awake.py
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

with open("keep_awake.py", "w", encoding="utf-8") as f:
    f.write(bot_code)

with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write(req_code)

with open(".github/workflows/keep_awake.yml", "w", encoding="utf-8") as f:
    f.write(yaml_code)
