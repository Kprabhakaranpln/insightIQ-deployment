import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ---------------------------------------------------------------------------
# 1. Page configuration & Material Styling
# ---------------------------------------------------------------------------
st.set_page_config(page_title="InsightIQ | Data Refinery", page_icon="🧭", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

:root {
    --md-primary: #6750A4;
    --md-on-primary: #FFFFFF;
    --md-background: #F3F4F6;
    --md-surface: #FFFFFF;
    --md-on-surface: #1C1B1F;
    --md-on-surface-variant: #49454F;
    --md-outline: #CAC4D0;
    --md-elevation-1: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    --md-elevation-2: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
}

html, body, [class*="css"] { 
    font-family: 'Roboto', sans-serif !important; 
    color: var(--md-on-surface);
}
header { visibility: hidden; }

.stApp { background-color: var(--md-background); }
.block-container { padding-top: 5rem !important; max-width: 1400px !important; }

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

section[data-testid="stSidebar"] { 
    background-color: var(--md-surface); 
    border-right: 1px solid var(--md-outline); 
}

/* Excel-like Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: var(--md-surface);
    padding: 4px 4px 0 4px;
    border-bottom: 2px solid var(--md-outline);
}
.stTabs [data-baseweb="tab"] {
    font-weight: 500;
    font-size: 13px;
    color: var(--md-on-surface-variant);
    padding: 10px 20px;
    border-radius: 8px 8px 0 0;
    background-color: transparent;
    transition: all 0.2s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background-color: rgba(103, 80, 164, 0.08);
}
.stTabs [aria-selected="true"] {
    color: var(--md-primary) !important;
    background-color: var(--md-surface) !important;
    border-bottom: 3px solid var(--md-primary) !important;
    box-shadow: var(--md-elevation-1);
}

/* Enhanced Metrics */
[data-testid="metric-container"] {
    background: var(--md-surface);
    border-radius: 12px;
    padding: 20px;
    box-shadow: var(--md-elevation-1);
    border-left: 4px solid var(--md-primary);
}

/* Quick Action Buttons */
.quick-action-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

/* Pivot Table Styling */
.pivot-container {
    background: var(--md-surface);
    border-radius: 12px;
    padding: 20px;
    box-shadow: var(--md-elevation-1);
}

/* Mini Chart Cards */
.chart-card {
    background: var(--md-surface);
    border-radius: 12px;
    padding: 16px;
    box-shadow: var(--md-elevation-1);
    margin: 8px 0;
}

footer, #MainMenu { visibility: hidden; }

.pill {
    display: inline-block;
    font-size: 11px;
    letter-spacing: 0.5px;
    padding: 4px 12px;
    margin: 2px 4px 2px 0;
    border: 1px solid var(--md-outline);
    border-radius: 16px;
    color: var(--md-on-surface-variant);
    background: var(--md-surface);
    font-weight: 500;
    text-transform: uppercase;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #4CAF50;
    margin-right: 8px;
}
</style>

<div class="sticky-header">
    <div style="display:flex; align-items:center; width:100%;">
        <span class="emoji-icon">📊</span>
        <h1 class="sticky-title">InsightIQ <span style="font-size:14px; color:var(--md-on-surface-variant); font-weight:400; margin-left:8px;">Data Refinery</span></h1>
        <div style="margin-left:auto; display:flex; gap:16px; align-items:center;">
            <span class="status-dot"></span>
            <span style="font-size:13px; color:var(--md-on-surface-variant);">Live</span>
        </div>
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

def create_pivot_table(df, index_col, columns_col, values_col, agg_func='sum'):
    """Create a pivot table with error handling"""
    try:
        if agg_func == 'sum':
            pivot = pd.pivot_table(df, values=values_col, index=index_col, 
                                   columns=columns_col, aggfunc=np.sum, fill_value=0)
        elif agg_func == 'mean':
            pivot = pd.pivot_table(df, values=values_col, index=index_col, 
                                   columns=columns_col, aggfunc=np.mean, fill_value=0)
        elif agg_func == 'count':
            pivot = pd.pivot_table(df, values=values_col, index=index_col, 
                                   columns=columns_col, aggfunc='count', fill_value=0)
        elif agg_func == 'max':
            pivot = pd.pivot_table(df, values=values_col, index=index_col, 
                                   columns=columns_col, aggfunc=np.max, fill_value=0)
        elif agg_func == 'min':
            pivot = pd.pivot_table(df, values=values_col, index=index_col, 
                                   columns=columns_col, aggfunc=np.min, fill_value=0)
        return pivot
    except Exception as e:
        st.error(f"Could not create pivot table: {e}")
        return None

# ---------------------------------------------------------------------------
# 3. Sidebar
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
            
            # Quick Stats
            st.markdown("---")
            st.caption("Quick Insights")
            numeric_cols = df_active.select_dtypes(include="number").columns
            if len(numeric_cols) > 0:
                st.metric("Numeric Columns", len(numeric_cols))
                st.metric("Avg Numeric Value", f"{df_active[numeric_cols].mean().mean():.2f}")
    else:
        st.caption("No data loaded yet — upload a file above to begin.")

# ---------------------------------------------------------------------------
# 4. Main workspace
# ---------------------------------------------------------------------------
if "df" in st.session_state:
    
    # Top Toolbar
    st.markdown("### ⏳ Data Timeline")
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

    # Excel-like Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📋 Data View", "🧹 Cleaning", "📊 Pivot Table", 
        "📈 Charts", "🎨 Dashboard", "⚙️ Processing", 
        "💡 Notes", "📤 Export"
    ])

    # --- Tab 1: Data View (Excel-like) ---
    with tab1:
        st.markdown("### 📋 Data View")
        df = st.session_state["df"]
        
        # Quick filters
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            filter_col = st.selectbox("Filter by column", ["None"] + df.columns.tolist())
        with col2:
            if filter_col != "None":
                unique_vals = df[filter_col].unique().tolist()
                filter_val = st.selectbox("Select value", unique_vals)
        with col3:
            rows_to_show = st.selectbox("Rows", [50, 100, 200, 500, "All"])
        
        # Apply filter
        filtered_df = df.copy()
        if filter_col != "None" and filter_val:
            filtered_df = filtered_df[filtered_df[filter_col] == filter_val]
        
        # Show data
        if rows_to_show != "All":
            st.dataframe(filtered_df.head(rows_to_show), use_container_width=True, height=400)
        else:
            st.dataframe(filtered_df, use_container_width=True, height=400)
        
        st.caption(f"Showing {len(filtered_df)} of {len(df)} rows")

    # --- Tab 2: Cleaning (Improved) ---
    with tab2:
        st.markdown("### 🧹 Data Cleaning")
        df = st.session_state["df"]

        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("Total Rows", f"{len(df):,}")
        with colB:
            missing_pct = (df.isna().sum().sum() / df.size * 100) if df.size else 0
            st.metric("Missing Data", f"{missing_pct:.1f}%")
        with colC:
            duplicates = int(df.duplicated().sum())
            st.metric("Duplicates", duplicates)

        # Quick cleaning actions
        st.markdown("#### Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🗑️ Drop Duplicates", use_container_width=True):
                if duplicates > 0:
                    commit_action(df.drop_duplicates())
                    st.rerun()
                else:
                    st.info("No duplicates found!")
        
        with col2:
            if st.button("🚫 Drop Missing Rows", use_container_width=True):
                if missing_pct > 0:
                    commit_action(df.dropna())
                    st.rerun()
                else:
                    st.info("No missing data found!")
        
        with col3:
            fill_method = st.selectbox("Fill with", ["Mean", "Median", "Mode", "0"], key="fill_method")
            if st.button("🩹 Fill Missing", use_container_width=True):
                df_filled = df.copy()
                for col in df_filled.columns:
                    if df_filled[col].isna().any():
                        if fill_method == "Mean" and pd.api.types.is_numeric_dtype(df_filled[col]):
                            df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
                        elif fill_method == "Median" and pd.api.types.is_numeric_dtype(df_filled[col]):
                            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
                        elif fill_method == "Mode":
                            mode_vals = df_filled[col].mode()
                            df_filled[col] = df_filled[col].fillna(mode_vals.iloc[0] if not mode_vals.empty else "")
                        elif fill_method == "0":
                            df_filled[col] = df_filled[col].fillna(0)
                commit_action(df_filled)
                st.rerun()
        
        with col4:
            if st.button("🔄 Reset Data", use_container_width=True):
                commit_action(st.session_state["datasets"][st.session_state["active_name"]].copy())
                st.rerun()

    # --- Tab 3: Pivot Table (New) ---
    with tab3:
        st.markdown("### 📊 Pivot Table")
        df = st.session_state["df"]
        
        # Create pivot table interface
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            index_col = st.selectbox("Rows (Index)", df.columns.tolist())
        with col2:
            columns_col = st.selectbox("Columns", df.columns.tolist())
        with col3:
            values_col = st.selectbox("Values", df.columns.tolist())
        with col4:
            agg_func = st.selectbox("Aggregation", ["sum", "mean", "count", "max", "min"])
        
        if st.button("🔄 Generate Pivot Table", use_container_width=True):
            pivot_df = create_pivot_table(df, index_col, columns_col, values_col, agg_func)
            if pivot_df is not None:
                st.session_state["pivot_df"] = pivot_df
        
        if "pivot_df" in st.session_state:
            st.markdown("#### Pivot Table Result")
            st.dataframe(st.session_state["pivot_df"], use_container_width=True, height=400)
            
            # Export pivot
            if st.button("📥 Export Pivot Table"):
                csv = st.session_state["pivot_df"].to_csv()
                st.download_button(
                    "⬇️ Download CSV", 
                    csv, 
                    file_name="pivot_table.csv",
                    mime="text/csv"
                )

    # --- Tab 4: Charts (Enhanced) ---
    with tab4:
        st.markdown("### 📈 Charts")
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()
        
        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Box Plot", "Area Chart"]
        )
        
        st.markdown("---")
        
        if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Area Chart"]:
            c1, c2, c3 = st.columns(3)
            with c1: x_axis = st.selectbox("X-Axis", all_cols)
            with c2: y_axis = st.selectbox("Y-Axis", numeric_cols)
            with c3: color_col = st.selectbox("Color by", ["None"] + all_cols)
            
            color_param = None if color_col == "None" else color_col
            
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_param, 
                            text_auto='.2s', title=f"{y_axis} by {x_axis}")
                fig.update_traces(textposition="outside")
            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_param, 
                             markers=True, title=f"{y_axis} trend by {x_axis}")
            elif chart_type == "Scatter Plot":
                size_col = st.selectbox("Size by", ["None"] + numeric_cols)
                size_param = None if size_col == "None" else size_col
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_param, 
                                size=size_param, title=f"{y_axis} vs {x_axis}")
            elif chart_type == "Area Chart":
                fig = px.area(df, x=x_axis, y=y_axis, color=color_param,
                             title=f"{y_axis} area by {x_axis}")
            
            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font_family="Roboto",
                font_color="#49454F",
                showlegend=True,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Quick stats
            with st.expander("📊 Summary Statistics"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Mean", f"{df[y_axis].mean():.2f}")
                with col2:
                    st.metric("Median", f"{df[y_axis].median():.2f}")
                with col3:
                    st.metric("Std Dev", f"{df[y_axis].std():.2f}")
        
        elif chart_type == "Pie Chart":
            c1, c2 = st.columns(2)
            with c1: names = st.selectbox("Categories", all_cols)
            with c2: values = st.selectbox("Values", numeric_cols)
            
            fig = px.pie(df, names=names, values=values, 
                        title=f"Distribution of {names}",
                        hole=0.3)
            fig.update_traces(textinfo='label+percent', textposition='inside')
            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font_family="Roboto",
                font_color="#49454F"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type in ["Histogram", "Box Plot"]:
            target_col = st.selectbox("Select Column", numeric_cols)
            
            if chart_type == "Histogram":
                bins = st.slider("Number of bins", 5, 50, 20)
                fig = px.histogram(df, x=target_col, nbins=bins,
                                  title=f"Distribution of {target_col}",
                                  text_auto=True)
                fig.update_traces(marker_color="#6750A4")
            else:
                fig = px.box(df, y=target_col, title=f"Box Plot of {target_col}",
                            points="all")
                fig.update_traces(marker_color="#6750A4")
            
            fig.update_layout(
                plot_bgcolor="#FFFFFF",
                paper_bgcolor="#FFFFFF",
                font_family="Roboto",
                font_color="#49454F"
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- Tab 5: Dashboard (Enhanced) ---
    with tab5:
        st.markdown("### 🎨 Interactive Dashboard")
        df = st.session_state["df"]
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        
        # Quick filters
        st.markdown("#### 🔍 Filters")
        filter_cols = st.multiselect("Filter by columns", df.columns.tolist())
        
        filtered_df = df.copy()
        for col in filter_cols:
            unique_vals = df[col].unique().tolist()
            selected_vals = st.multiselect(f"Select {col}", unique_vals, default=unique_vals[:2])
            if selected_vals:
                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
        
        st.markdown("---")
        
        # KPI Cards
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        with kpi1:
            st.metric("Total Records", f"{len(filtered_df):,}", 
                     delta=f"{len(filtered_df) - len(df):+d}" if len(filtered_df) != len(df) else None)
        with kpi2:
            if numeric_cols:
                st.metric("Average", f"{filtered_df[numeric_cols[0]].mean():.2f}")
        with kpi3:
            if len(numeric_cols) > 1:
                st.metric("Max Value", f"{filtered_df[numeric_cols[1]].max():.2f}")
        with kpi4:
            if len(numeric_cols) > 2:
                st.metric("Min Value", f"{filtered_df[numeric_cols[2]].min():.2f}")
        
        # Charts Grid
        col1, col2 = st.columns(2)
        
        with col1:
            if numeric_cols:
                fig1 = px.histogram(filtered_df, x=numeric_cols[0], 
                                    title=f"Distribution of {numeric_cols[0]}",
                                    color_discrete_sequence=["#6750A4"])
                fig1.update_layout(plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if len(numeric_cols) > 1:
                fig2 = px.box(filtered_df, y=numeric_cols[1],
                             title=f"Spread of {numeric_cols[1]}",
                             color_discrete_sequence=["#2196F3"])
                fig2.update_layout(plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")
                st.plotly_chart(fig2, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            if len(numeric_cols) > 1:
                fig3 = px.scatter(filtered_df, x=numeric_cols[0], y=numeric_cols[1],
                                 title=f"Correlation: {numeric_cols[0]} vs {numeric_cols[1]}",
                                 color_discrete_sequence=["#1C1B1F"])
                fig3.update_layout(plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")
                st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            if len(filtered_df.columns) > 1:
                # Top categories
                top_col = filtered_df.columns[0]
                top_data = filtered_df[top_col].value_counts().head(10)
                fig4 = px.bar(x=top_data.index, y=top_data.values,
                             title=f"Top {top_col} Categories",
                             color_discrete_sequence=["#FF6B6B"])
                fig4.update_layout(plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")
                st.plotly_chart(fig4, use_container_width=True)

    # --- Tab 6: Processing (Enhanced) ---
    with tab6:
        st.markdown("### ⚙️ Data Processing")
        df = st.session_state["df"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Column Operations")
            cols_to_drop = st.multiselect("Select columns to drop", df.columns.tolist())
            if st.button("🗑️ Drop Selected Columns", use_container_width=True) and cols_to_drop:
                commit_action(df.drop(columns=cols_to_drop))
                st.rerun()
        
        with col2:
            st.markdown("#### Rename Column")
            col_to_rename = st.selectbox("Select column", df.columns.tolist())
            new_name = st.text_input("New name")
            if st.button("✏️ Rename", use_container_width=True) and new_name:
                commit_action(df.rename(columns={col_to_rename: new_name}))
                st.rerun()
        
        st.markdown("---")
        
        # Data type conversion
        st.markdown("#### Data Type Conversion")
        col_to_convert = st.selectbox("Select column to convert", df.columns.tolist())
        new_type = st.selectbox("Convert to", ["int", "float", "str", "datetime"])
        
        if st.button("🔄 Convert Data Type", use_container_width=True):
            df_converted = df.copy()
            try:
                if new_type == "int":
                    df_converted[col_to_convert] = pd.to_numeric(df_converted[col_to_convert], errors='coerce').astype('Int64')
                elif new_type == "float":
                    df_converted[col_to_convert] = pd.to_numeric(df_converted[col_to_convert], errors='coerce')
                elif new_type == "str":
                    df_converted[col_to_convert] = df_converted[col_to_convert].astype(str)
                elif new_type == "datetime":
                    df_converted[col_to_convert] = pd.to_datetime(df_converted[col_to_convert], errors='coerce')
                commit_action(df_converted)
                st.rerun()
            except Exception as e:
                st.error(f"Conversion failed: {e}")

    # --- Tab 7: Notes ---
    with tab7:
        st.markdown("### 💡 Analysis Notes")
        if "analyst_notes" not in st.session_state:
            st.session_state["analyst_notes"] = ""
        
        st.session_state["analyst_notes"] = st.text_area(
            "📝 Record your observations, insights, and next steps:",
            value=st.session_state["analyst_notes"],
            height=400
        )
        
        if st.button("💾 Save Notes"):
            st.success("Notes saved successfully!")

    # --- Tab 8: Export ---
    with tab8:
        st.markdown("### 📤 Export Data")
        df = st.session_state["df"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Export as CSV**")
            st.download_button(
                "⬇️ Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="insightiq_export.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Export as Excel**")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button(
                "⬇️ Download Excel",
                buffer.getvalue(),
                file_name="insightiq_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            st.markdown("**Export as JSON**")
            st.download_button(
                "⬇️ Download JSON",
                df.to_json(orient="records", indent=2),
                file_name="insightiq_export.json",
                mime="application/json",
                use_container_width=True
            )
        
        st.markdown("---")
        st.markdown("**Export Options**")
        
        # Export options
        export_selected = st.multiselect("Select specific columns to export", df.columns.tolist())
        if export_selected and st.button("📥 Export Selected Columns"):
            export_df = df[export_selected]
            st.download_button(
                "⬇️ Download Selected Columns",
                export_df.to_csv(index=False).encode("utf-8"),
                file_name="insightiq_selected_export.csv",
                mime="text/csv",
                use_container_width=True
            )

else:
    st.markdown("""
    <div style="text-align:center; padding: 80px 20px; background: var(--md-surface); border-radius: 12px; box-shadow: var(--md-elevation-1);">
        <h3 style="font-size: 28px; color: var(--md-primary);">📂 Ready for Data</h3>
        <p style="font-size: 16px; color: var(--md-on-surface-variant); margin: 16px 0;">
            Upload a file from the Workspace in the sidebar to begin processing.
        </p>
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: 24px; flex-wrap: wrap;">
            <span class="pill">CSV</span>
            <span class="pill">Excel</span>
            <span class="pill">JSON</span>
            <span class="pill">XML</span>
            <span class="pill">Parquet</span>
            <span class="pill">Avro</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('''
<div style="text-align:center; color:var(--md-on-surface-variant); font-size:12px; margin-top:60px; padding:20px 0; letter-spacing:1px; border-top: 1px solid var(--md-outline);">
    INSIGHTIQ • DATA REFINERY • v2.0
</div>
''', unsafe_allow_html=True)
