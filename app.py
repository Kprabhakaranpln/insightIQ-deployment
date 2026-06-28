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
    --paper: #F8FAFC;
    --ink: #0F172A;
    --teal: #2563EB;
    --copper: #7C3AED;
    --slate: #475569;
    --line: #E2E8F0;
}

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }

/* Keep default header for the hamburger menu, but make it invisible and hide the right-side clutter */
header { background-color: transparent !important; }
[data-testid="stHeaderActionElements"] { display: none; }

.sticky-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    z-index: 99998; /* Lowered slightly to not block the hamburger */
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 14px 0;
    padding-left: 60px; /* Added padding so title doesn't overlap with hamburger */
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

.emoji-icon { font-size: 28px; margin-right: 10px; }
.stApp { background-color: var(--paper); }
.block-container { padding-top: 5rem !important; max-width: 1100px !important; }
section[data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid var(--line); }

.hero-minimal { text-align: center; padding: 20px 0 8px 0; }
.hero-minimal h1 { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 42px; color: var(--ink); margin: 0 0 6px 0; letter-spacing: -1px; }
.hero-minimal .subtitle { font-family: 'IBM Plex Sans', sans-serif; font-size: 16px; color: var(--slate); max-width: 500px; margin: 0 auto; line-height: 1.5; }

.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; max-width: 800px; margin: 16px auto 0 auto; padding: 0 20px; }
.feature-item { background: #FFFFFF; border: 1px solid var(--line); border-radius: 8px; padding: 16px 12px; text-align: center; transition: all 0.15s ease; }
.feature-item:hover { border-color: var(--teal); box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06); }
.feature-item .icon { font-size: 22px; display: block; margin-bottom: 4px; }
.feature-item .label { font-family: 'IBM Plex Sans', sans-serif; font-size: 13px; font-weight: 500; color: var(--ink); }
.feature-item .desc { font-family: 'IBM Plex Sans', sans-serif; font-size: 12px; color: var(--slate); margin: 0; }

.dash-divider { border: none; border-top: 1px solid var(--line); margin: 16px 0 20px 0; opacity: 0.6; }
.empty-state { border: 1px dashed var(--line); border-radius: 8px; padding: 48px 24px; text-align: center; background: #FFFFFF; }
.empty-state h3 { font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 600; color: var(--ink); margin: 0 0 4px 0; }
.empty-state p { font-family: 'IBM Plex Sans', sans-serif; color: var(--slate); font-size: 14px; margin: 0; }

.stTabs [data-baseweb="tab-list"] { gap: 2px; border-bottom: 1px solid var(--line); flex-wrap: wrap; background: transparent; }
.stTabs [data-baseweb="tab"] { font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 0.02em; color: var(--slate); padding: 8px 16px; border-radius: 6px 6px 0 0; }
.stTabs [aria-selected="true"] { color: var(--ink) !important; border-bottom: 2px solid var(--teal) !important; font-weight: 600; background: transparent !important; }

.stButton > button { font-family: 'IBM Plex Sans', sans-serif; border: 1px solid var(--line); background-color: #FFFFFF; color: var(--ink); border-radius: 6px; font-weight: 500; font-size: 13px; transition: all 0.15s ease; }
.stButton > button:hover { background-color: var(--ink); color: #FFFFFF; border-color: var(--ink); }

[data-testid="metric-container"] { background: #FFFFFF; border: 1px solid var(--line); border-radius: 8px; padding: 12px; box-shadow: none; }
footer, #MainMenu { visibility: hidden; }

.status-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #22C55E; margin-right: 6px; }
.status-text { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--slate); }
.pill { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 10px; letter-spacing: 0.04em; padding: 2px 10px; margin: 2px 3px 2px 0; border: 1px solid var(--line); border-radius: 999px; color: var(--slate); background: #FFFFFF; }
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center;">
        <span class="emoji-icon">🧠</span>
        <h1 class="sticky-title">InsightIQ</h1>
        <span style="margin-left:12px; font-family:'IBM Plex Mono',monospace; font-size:11px; color:var(--slate); font-weight:400;">data refinery</span>
    </div>
</div>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

# ---------------------------------------------------------------------------
# 2. Hero Section
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-minimal">
    <h1>Clean, analyze, visualize</h1>
    <p class="subtitle">Upload any dataset and go from raw to insights in minutes</p>
</div>
<div class="feature-grid">
    <div class="feature-item">
        <span class="icon">📥</span>
        <div class="label">Import</div>
        <p class="desc">8 formats supported</p>
    </div>
    <div class="feature-item">
        <span class="icon">🧹</span>
        <div class="label">Clean</div>
        <p class="desc">Remove noise & fix data</p>
    </div>
    <div class="feature-item">
        <span class="icon">📊</span>
        <div class="label">Visualize</div>
        <p class="desc">Interactive charts & dashboards</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align:center; margin: 12px 0 8px 0;">
        <span class="status-dot"></span>
        <span class="status-text">Ready · {len(SUPPORTED_FORMATS)} formats · {" · ".join(f.upper() for f in SUPPORTED_FORMATS)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<hr class="dash-divider">', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3. Core Logic Functions
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
    st.session_state["df_history"] = st.session_state["df_history"][:current_idx + 1]
    st.session_state["df_history"].append(new_df.copy())
    st.session_state["history_index"] += 1
    st.session_state["df"] = new_df.copy()

# ---------------------------------------------------------------------------
# 4. Sidebar — Command Center
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
            
            # Setup initial dataframe and history timeline
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
    else:
        st.caption("No data loaded yet — upload a file above to begin.")

# ---------------------------------------------------------------------------
# 5. Main workspace
# ---------------------------------------------------------------------------
if "df" in st.session_state:
    
    # --- TOP TOOLBAR (Undo/Redo) ---
    st.markdown("### ⏳ Data Timeline & Actions")
    toolbar_col1, toolbar_col2, toolbar_col3 = st.columns([6, 1, 1])
    
    with toolbar_col1:
        st.info(f"**Current Dataset:** `{st.session_state['active_name']}` | **Modifications:** `{st.session_state['history_index']}`")
    
    can_undo = st.session_state["history_index"] > 0
    can_redo = st.session_state["history_index"] < len(st.session_state["df_history"]) - 1
    
    with toolbar_col2:
        if st.button("⏪ Undo", disabled=not can_undo, use_container_width=True):
            st.session_state["history_index"] -= 1
            st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
            st.rerun()
    with toolbar_col3:
        if st.button("⏩ Redo", disabled=not can_redo, use_container_width=True):
            st.session_state["history_index"] += 1
            st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
            st.rerun()
            
    st.markdown("---")

    # --- TABS WORKSPACE ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧹 Data Cleaning", "⚙️ Data Processing", "📊 Data Analysis", 
        "📈 Data Visualize", "💡 Interpretation", "🎯 Decision Making"
    ])

    # --- Tab 1: Data Cleaning ---
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

    # --- Tab 2: Data Processing ---
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

    # --- Tab 3: Data Analysis & Pivot (UPDATED WITH MULTIPLE PIVOTS) ---
    with tab3:
        st.markdown('<p class="stage-eyebrow">Stage 03</p>', unsafe_allow_html=True)
        st.markdown("### 📊 Data Analysis & Pivot")
        df = st.session_state["df"]
        
        st.markdown("#### Summary Statistics")
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🔀 Pivot Table Generator")
        
        # Initialize pivot storage if not exists
        if "pivot_results" not in st.session_state:
            st.session_state["pivot_results"] = []
        
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        
        # Pivot creation form
        with st.form("pivot_form"):
            st.markdown("##### Create New Pivot Table")
            p_col1, p_col2, p_col3 = st.columns(3)
            with p_col1:
                pivot_index = st.selectbox("Rows (Index)", ["None"] + all_cols)
            with p_col2:
                pivot_values = st.selectbox("Values to Aggregate", ["None"] + numeric_cols)
            with p_col3:
                pivot_agg = st.selectbox("Aggregation Function", ["mean", "sum", "count", "max", "min"])
            
            pivot_name = st.text_input("Pivot Table Name (optional)", value=f"Pivot {len(st.session_state['pivot_results']) + 1}")
            create_pivot = st.form_submit_button("➕ Create Pivot Table", type="primary")

        # Create new pivot
        if create_pivot and pivot_index != "None" and pivot_values != "None":
            try:
                pivot_df = pd.pivot_table(
                    df, 
                    index=pivot_index, 
                    values=pivot_values, 
                    aggfunc=pivot_agg
                ).reset_index()
                
                # Store pivot in session state
                st.session_state["pivot_results"].append({
                    "name": pivot_name,
                    "df": pivot_df,
                    "index": pivot_index,
                    "value": pivot_values,
                    "agg": pivot_agg
                })
                st.success(f"✅ Pivot table '{pivot_name}' created successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Could not generate pivot table: {e}")
        
        st.markdown("---")
        
        # Display all stored pivots
        if st.session_state["pivot_results"]:
            st.markdown(f"### 📋 Saved Pivot Tables ({len(st.session_state['pivot_results'])})")
            
            # Create tabs for each pivot
            pivot_names = [p["name"] for p in st.session_state["pivot_results"]]
            pivot_tabs = st.tabs(pivot_names)
            
            for i, tab in enumerate(pivot_tabs):
                with tab:
                    pivot_data = st.session_state["pivot_results"][i]
                    pdf = pivot_data["df"]
                    
                    st.caption(f"**{pivot_data['agg'].upper()}** of **{pivot_data['value']}** by **{pivot_data['index']}**")
                    
                    # Display pivot table
                    st.dataframe(pdf, use_container_width=True)
                    
                    # Visualization
                    chart_theme = dict(
                        plot_bgcolor="#F8FAFC", 
                        paper_bgcolor="#F8FAFC", 
                        font_family="IBM Plex Sans"
                    )
                    
                    try:
                        fig = px.bar(
                            pdf, 
                            x=pivot_data["index"], 
                            y=pivot_data["value"],
                            title=f"{pivot_data['name']} - Visualization",
                            color=pivot_data["value"],
                            color_continuous_scale="Viridis"
                        )
                        fig.update_layout(**chart_theme)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not generate chart: {e}")
                    
                    # Export options for this pivot
                    csv = pdf.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        f"⬇️ Download {pivot_data['name']} as CSV",
                        csv,
                        f"{pivot_data['name']}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            
            st.markdown("---")
            
            # Delete pivot option
            st.markdown("### 🗑️ Manage Pivots")
            delete_col1, delete_col2 = st.columns([3, 1])
            with delete_col1:
                pivot_to_delete = st.selectbox(
                    "Select pivot to delete", 
                    pivot_names,
                    key="delete_pivot_selector"
                )
            with delete_col2:
                if st.button("🗑️ Delete Selected", type="secondary", use_container_width=True):
                    # Find index and remove
                    for idx, p in enumerate(st.session_state["pivot_results"]):
                        if p["name"] == pivot_to_delete:
                            st.session_state["pivot_results"].pop(idx)
                            st.success(f"Deleted '{pivot_to_delete}'")
                            st.rerun()
                            break
            
            # Clear all pivots
            if st.button("🗑️ Clear All Pivots", type="secondary"):
                st.session_state["pivot_results"] = []
                st.rerun()
                
        else:
            st.info("No pivot tables created yet. Use the form above to create your first pivot.")

    # --- Tab 4: Data Visualize ---
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
                c1, c2, c3 = st.columns(3)
                with c1: x_axis = st.selectbox("X-Axis", all_cols)
                with c2: y_axis = st.selectbox("Y-Axis", numeric_cols)
                with c3: color_col = st.selectbox("Color by (Optional)", ["None"] + all_cols)
                
                color_param = None if color_col == "None" else color_col
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

    # --- Tab 5: Interpretation ---
    with tab5:
        st.markdown('<p class="stage-eyebrow">Stage 05</p>', unsafe_allow_html=True)
        st.markdown("### 💡 Interpretation")
        if "analyst_notes" not in st.session_state: st.session_state["analyst_notes"] = ""
        st.session_state["analyst_notes"] = st.text_area("Observations:", value=st.session_state["analyst_notes"], height=300)

    # --- Tab 6: Decision Making ---
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
