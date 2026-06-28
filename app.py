import io
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------------------------
# 1. Page configuration & Material Styling
# ---------------------------------------------------------------------------
st.set_page_config(page_title="InsightIQ | Data Refinery", page_icon="🧭", layout="wide")

st.markdown("""
<style>
/* Import official Material Design font */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

:root {
    /* Material 3 Color Palette */
    --md-primary: #6750A4; 
    --md-on-primary: #FFFFFF;
    --md-background: #F3F4F6;
    --md-surface: #FFFFFF;
    --md-on-surface: #1C1B1F;
    --md-on-surface-variant: #49454F;
    --md-outline: #CAC4D0;
    
    /* Material Elevations (Shadows) */
    --md-elevation-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    --md-elevation-2: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
}

html, body, [class*="css"] { 
    font-family: 'Roboto', sans-serif !important; 
    color: var(--md-on-surface);
}
header { visibility: hidden; }

.stApp { background-color: var(--md-background); }
.block-container { padding-top: 5rem !important; max-width: 1100px !important; }

/* Material App Bar */
.sticky-header {
    position: fixed;
    top: 0; left: 0; width: 100%;
    background-color: var(--md-surface);
    box-shadow: var(--md-elevation-1);
    z-index: 99999;
    display: flex;
    align-items: center;
    padding: 14px 24px;
}
.sticky-title {
    font-weight: 500; 
    font-size: 22px; 
    margin: 0; 
    letter-spacing: 0.15px;
    color: var(--md-on-surface);
}
.emoji-icon { font-size: 24px; margin-right: 12px; }

/* Sidebar styling */
section[data-testid="stSidebar"] { 
    background-color: var(--md-surface); 
    border-right: 1px solid var(--md-outline); 
}

/* Hero Section */
.hero-minimal { text-align: center; padding: 24px 0 16px 0; }
.hero-minimal h1 { font-weight: 700; font-size: 40px; color: var(--md-primary); margin: 0 0 8px 0; letter-spacing: -0.5px; }
.hero-minimal .subtitle { font-size: 16px; color: var(--md-on-surface-variant); max-width: 500px; margin: 0 auto; line-height: 1.5; }

/* Material Cards for Features */
.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 800px; margin: 24px auto 0 auto; padding: 0 20px; }
.feature-item { 
    background: var(--md-surface); 
    border-radius: 12px; 
    box-shadow: var(--md-elevation-1); 
    padding: 20px 16px; 
    text-align: center; 
    transition: box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1); 
}
.feature-item:hover { box-shadow: var(--md-elevation-2); }
.feature-item .icon { font-size: 28px; display: block; margin-bottom: 8px; color: var(--md-primary); }
.feature-item .label { font-size: 14px; font-weight: 500; color: var(--md-on-surface); letter-spacing: 0.1px; }
.feature-item .desc { font-size: 13px; color: var(--md-on-surface-variant); margin: 4px 0 0 0; }

.dash-divider { border: none; border-top: 1px solid var(--md-outline); margin: 24px 0; opacity: 0.5; }

/* Empty State Card */
.empty-state { 
    border-radius: 12px; 
    padding: 48px 24px; 
    text-align: center; 
    background: var(--md-surface);
    box-shadow: var(--md-elevation-1);
}
.empty-state h3 { font-size: 20px; font-weight: 500; color: var(--md-on-surface); margin: 0 0 8px 0; }
.empty-state p { color: var(--md-on-surface-variant); font-size: 15px; margin: 0; }

/* Material Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid var(--md-outline); background: transparent; }
.stTabs [data-baseweb="tab"] { 
    font-weight: 500; 
    font-size: 14px; 
    color: var(--md-on-surface-variant); 
    padding: 12px 16px; 
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.stTabs [aria-selected="true"] { 
    color: var(--md-primary) !important; 
    border-bottom: 3px solid var(--md-primary) !important; 
    background: transparent !important; 
}

/* Material Buttons (Pill shaped M3) */
.stButton > button { 
    background-color: transparent; 
    color: var(--md-primary); 
    border: 1px solid var(--md-outline); 
    border-radius: 100px; 
    font-weight: 500; 
    font-size: 14px; 
    letter-spacing: 0.1px;
    padding: 8px 24px;
    transition: background-color 0.2s ease, border-color 0.2s ease; 
}
.stButton > button:hover { 
    background-color: rgba(103, 80, 164, 0.08); 
    border-color: var(--md-primary); 
    color: var(--md-primary);
}

/* Material Metrics Cards */
[data-testid="metric-container"] { 
    background: var(--md-surface); 
    border-radius: 12px; 
    padding: 16px; 
    box-shadow: var(--md-elevation-1);
    border: none;
}
[data-testid="metric-container"] label {
    color: var(--md-on-surface-variant) !important;
    font-weight: 500;
}

footer, #MainMenu { visibility: hidden; }

.status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #4CAF50; margin-right: 8px; }
.status-text { font-size: 13px; color: var(--md-on-surface-variant); font-weight: 500; }
.pill { display: inline-block; font-size: 11px; letter-spacing: 0.5px; padding: 4px 12px; margin: 2px 4px 2px 0; border: 1px solid var(--md-outline); border-radius: 16px; color: var(--md-on-surface-variant); background: var(--md-surface); font-weight: 500; text-transform: uppercase; }
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center;">
        <span class="emoji-icon">📊</span>
        <h1 class="sticky-title">InsightIQ <span style="font-size:14px; color:var(--md-on-surface-variant); font-weight:400; margin-left:8px;">Data Refinery</span></h1>
    </div>
</div>
""", unsafe_allow_html=True)

SUPPORTED_FORMATS = ["csv", "xlsx", "xls", "json", "jsonl", "xml", "parquet", "avro"]

# ---------------------------------------------------------------------------
# 2. Hero Section
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-minimal">
    <h1>Refine your data.</h1>
    <p class="subtitle">Upload any dataset and go from raw numbers to actionable insights instantly.</p>
</div>
<div class="feature-grid">
    <div class="feature-item">
        <span class="icon">upload_file</span>
        <div class="label">Import</div>
        <p class="desc">8 formats supported</p>
    </div>
    <div class="feature-item">
        <span class="icon">auto_fix_high</span>
        <div class="label">Clean</div>
        <p class="desc">Remove noise & fix data</p>
    </div>
    <div class="feature-item">
        <span class="icon">query_stats</span>
        <div class="label">Visualize</div>
        <p class="desc">Interactive dashboards</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align:center; margin: 24px 0 8px 0;">
        <span class="status-dot"></span>
        <span class="status-text">System Ready · {len(SUPPORTED_FORMATS)} formats · {" · ".join(f.upper() for f in SUPPORTED_FORMATS)}</span>
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
    current_idx = st.session_state["history_index"]
    st.session_state["df_history"] = st.session_state["df_history"][:current_idx + 1]
    st.session_state["df_history"].append(new_df.copy())
    st.session_state["history_index"] += 1
    st.session_state["df"] = new_df.copy()

# ---------------------------------------------------------------------------
# 4. Sidebar — Command Center
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚡ Workspace")
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
            
            if st.session_state.get("active_name") != active_name or "df_history" not in st.session_state:
                st.session_state["active_name"] = active_name
                initial_df = st.session_state["datasets"][active_name].copy()
                st.session_state["df_history"] = [initial_df]
                st.session_state["history_index"] = 0
                st.session_state["df"] = initial_df.copy()

            df_active = st.session_state["df"]
            st.markdown("---")
            c1, c2 = st.columns(2)
            c1.metric("Total Rows", f"{df_active.shape[0]:,}")
            c2.metric("Total Columns", df_active.shape[1])
    else:
        st.caption("No data loaded yet — upload a file above to begin.")

# ---------------------------------------------------------------------------
# 5. Main workspace & Tabs
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

    # --- TABS ---
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧹 Cleaning", "⚙️ Processing", "📊 Analysis", 
        "📈 Visualize", "💡 Interpretation", "🎯 Decision"
    ])

    # --- Tab 1: Data Cleaning ---
    with tab1:
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

    # --- Tab 3: Data Analysis ---
    with tab3:
        st.markdown("### 📊 Data Analysis")
        df = st.session_state["df"]
        st.markdown("#### Summary Statistics")
        st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

    # --- Tab 4: Data Visualize ---
    with tab4:
        st.markdown("### 📈 Data Visualize")
        
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        
        # Updated chart theme for Material Design
        chart_theme = dict(
            plot_bgcolor="#FFFFFF", 
            paper_bgcolor="#FFFFFF", 
            font_family="Roboto", 
            font_color="#49454F",
            margin=dict(t=40, b=40, l=40, r=40)
        )

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
                    st.markdown("#### 📝 Summary")
                    st.caption(f"Analyzing **{y_axis}** by **{x_axis}**")
                    st.write("**Top 5 Values:**")
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
                    st.markdown("#### 📝 Summary")
                    st.write("**Category Breakdown:**")
                    pie_data = df.groupby(names)[values].sum().reset_index().sort_values(by=values, ascending=False)
                    st.dataframe(pie_data, hide_index=True, use_container_width=True)

            elif chart_type == "Dashboard View":
                st.markdown("#### 🚀 Insights Dashboard")
                if len(numeric_cols) >= 1 and len(all_cols) >= 2:
                    d_col1, d_col2 = st.columns(2)
                    with d_col1:
                        fig1 = px.histogram(df, x=numeric_cols[0], title=f"Distribution of {numeric_cols[0]}", text_auto=True, color_discrete_sequence=["#6750A4"])
                        fig1.update_layout(**chart_theme)
                        st.plotly_chart(fig1, use_container_width=True)
                        
                        fig2 = px.pie(df, names=all_cols[0], title=f"Breakdown of {all_cols[0]}")
                        fig2.update_traces(textinfo='percent+label')
                        fig2.update_layout(**chart_theme)
                        st.plotly_chart(fig2, use_container_width=True)
                    with d_col2:
                        fig3 = px.box(df, y=numeric_cols[0], title=f"Spread of {numeric_cols[0]}", color_discrete_sequence=["#2196F3"])
                        fig3.update_layout(**chart_theme)
                        st.plotly_chart(fig3, use_container_width=True)
                        
                        if len(numeric_cols) >= 2:
                            fig4 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title=f"{numeric_cols[0]} vs {numeric_cols[1]}", color_discrete_sequence=["#1C1B1F"])
                            fig4.update_layout(**chart_theme)
                            st.plotly_chart(fig4, use_container_width=True)
                else:
                    st.warning("Not enough numeric/categorical data to generate a dashboard.")
                    
            elif chart_type == "Histogram":
                target_col = st.selectbox("Select Column to Analyze", numeric_cols)
                chart_col, data_col = st.columns([3, 1])
                
                with chart_col:
                    fig = px.histogram(df, x=target_col, text_auto=True, color_discrete_sequence=["#6750A4"])
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
        st.markdown("### 💡 Interpretation")
        if "analyst_notes" not in st.session_state: st.session_state["analyst_notes"] = ""
        st.session_state["analyst_notes"] = st.text_area("Observations:", value=st.session_state["analyst_notes"], height=300)

    # --- Tab 6: Decision Making ---
    with tab6:
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
        <h3>📂 Ready for Data</h3>
        <p>Upload a file from the Workspace in the sidebar to begin processing.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<p style="text-align:center;color:var(--md-on-surface-variant);font-size:12px;margin-top:40px;letter-spacing:1px;">INSIGHTIQ • DATA REFINERY</p>', unsafe_allow_html=True)
