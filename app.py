import io
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ---------------------------------------------------------------------------
# 1. Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="InsightIQ | Executive Dashboard", page_icon="📊", layout="wide")

# ---------------------------------------------------------------------------
# 2. Enhanced UI Design with Dashboard Focus
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #F8FAFC;
    --bg-secondary: #FFFFFF;
    --bg-card: #FFFFFF;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --border-color: #E2E8F0;
    --blue-500: #3B82F6;
    --blue-600: #2563EB;
    --indigo-500: #6366F1;
    --purple-500: #8B5CF6;
    --green-500: #22C55E;
    --red-500: #EF4444;
    --orange-500: #F59E0B;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

* { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

/* Hide Streamlit's default elements */
header, #MainMenu, footer { visibility: hidden; }
.stApp { background-color: var(--bg-primary); }

/* Custom Top Navigation */
.dashboard-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 99999;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    padding: 12px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.nav-brand h1 {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, var(--blue-600), var(--purple-500));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.nav-brand span {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    background: var(--bg-primary);
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid var(--border-color);
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 16px;
}

.nav-actions .status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--text-secondary);
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--green-500);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* Push content down */
.block-container {
    padding-top: 80px !important;
    max-width: 1400px !important;
    padding-left: 24px !important;
    padding-right: 24px !important;
}

/* KPI Cards Grid */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px 24px;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
}

.kpi-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--blue-500);
    transform: translateY(-2px);
}

.kpi-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.5px;
}

.kpi-change {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    font-weight: 500;
    margin-top: 8px;
    padding: 2px 10px;
    border-radius: 999px;
}

.kpi-change.positive {
    color: var(--green-500);
    background: rgba(34, 197, 94, 0.1);
}

.kpi-change.negative {
    color: var(--red-500);
    background: rgba(239, 68, 68, 0.1);
}

.kpi-change.neutral {
    color: var(--text-secondary);
    background: var(--bg-primary);
}

/* Filter Bar */
.filter-bar {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 24px;
    display: flex;
    gap: 16px;
    align-items: center;
    flex-wrap: wrap;
    box-shadow: var(--shadow-sm);
}

.filter-bar .filter-group {
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-bar label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    white-space: nowrap;
}

.filter-bar select, .filter-bar input {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 13px;
    background: var(--bg-primary);
    color: var(--text-primary);
    min-width: 120px;
}

.filter-bar select:focus, .filter-bar input:focus {
    outline: none;
    border-color: var(--blue-500);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Chart Container */
.chart-container {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 16px;
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.chart-header h3 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.chart-header .chart-actions {
    display: flex;
    gap: 8px;
}

.chart-header .chart-actions button {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s ease;
}

.chart-header .chart-actions button:hover {
    background: var(--blue-500);
    color: white;
    border-color: var(--blue-500);
}

/* Sidebar customization */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    padding-top: 80px;
}

section[data-testid="stSidebar"] .sidebar-content {
    padding: 20px;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
    .kpi-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 640px) {
    .kpi-grid {
        grid-template-columns: 1fr;
    }
    .dashboard-nav {
        padding: 12px 16px;
        flex-direction: column;
        gap: 8px;
    }
    .filter-bar {
        flex-direction: column;
        align-items: stretch;
    }
    .filter-bar .filter-group {
        flex-wrap: wrap;
    }
}

/* Utility classes */
.text-muted { color: var(--text-muted); }
.text-secondary { color: var(--text-secondary); }
.mb-2 { margin-bottom: 8px; }
.mb-4 { margin-bottom: 16px; }
.mt-4 { margin-top: 16px; }
.flex { display: flex; }
.gap-2 { gap: 8px; }
.gap-4 { gap: 16px; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
</style>

<!-- Navigation -->
<div class="dashboard-nav">
    <div class="nav-brand">
        <h1>📊 InsightIQ</h1>
        <span>Executive Dashboard</span>
    </div>
    <div class="nav-actions">
        <div class="status">
            <span class="status-dot"></span>
            <span>Live</span>
        </div>
        <span style="font-size:13px;color:var(--text-muted);">|</span>
        <span style="font-size:13px;color:var(--text-secondary);">
            Updated: <span id="current-time"></span>
        </span>
    </div>
</div>

<script>
    document.getElementById('current-time').textContent = new Date().toLocaleTimeString();
</script>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 3. Supported formats and core functions
# ---------------------------------------------------------------------------
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

def calculate_kpi_metrics(df):
    """Calculate key KPI metrics for the dashboard."""
    metrics = {
        "Total Records": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": df.isna().sum().sum(),
        "Duplicate Rows": df.duplicated().sum(),
        "Completeness": (1 - df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
    }
    
    # Add numeric metrics if available
    numeric_cols = df.select_dtypes(include=np.number).columns
    if len(numeric_cols) > 0:
        metrics["Total Value"] = df[numeric_cols[0]].sum()
        metrics["Average"] = df[numeric_cols[0]].mean()
        metrics["Max"] = df[numeric_cols[0]].max()
        metrics["Min"] = df[numeric_cols[0]].min()
    
    return metrics

# ---------------------------------------------------------------------------
# 4. Sidebar - Data Management
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🗂️ Data Management")
    
    uploaded_files = st.file_uploader("Upload Data", type=SUPPORTED_FORMATS, accept_multiple_files=True)
    
    if uploaded_files:
        if "datasets" not in st.session_state: st.session_state["datasets"] = {}
        for f in uploaded_files:
            if f.name not in st.session_state["datasets"]:
                loaded = load_dataset(f)
                if loaded is not None: 
                    st.session_state["datasets"][f.name] = loaded

        if st.session_state.get("datasets"):
            active_name = st.selectbox("Active Dataset", list(st.session_state["datasets"].keys()))
            
            if st.session_state.get("active_name") != active_name or "df_history" not in st.session_state:
                st.session_state["active_name"] = active_name
                initial_df = st.session_state["datasets"][active_name].copy()
                st.session_state["df_history"] = [initial_df]
                st.session_state["history_index"] = 0
                st.session_state["df"] = initial_df.copy()
            
            df = st.session_state["df"]
            
            st.markdown("---")
            st.markdown("### 📈 Data Timeline")
            
            col1, col2 = st.columns(2)
            can_undo = st.session_state["history_index"] > 0
            can_redo = st.session_state["history_index"] < len(st.session_state["df_history"]) - 1
            
            if col1.button("⏪ Undo", disabled=not can_undo, use_container_width=True):
                st.session_state["history_index"] -= 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()
                
            if col2.button("⏩ Redo", disabled=not can_redo, use_container_width=True):
                st.session_state["history_index"] += 1
                st.session_state["df"] = st.session_state["df_history"][st.session_state["history_index"]].copy()
                st.rerun()
            
            st.markdown("---")
            st.markdown("### 🧹 Quick Actions")
            
            if st.button("🧹 Auto Clean Data", use_container_width=True):
                df_cleaned = df.copy()
                # Remove duplicates
                df_cleaned = df_cleaned.drop_duplicates()
                # Fill numeric missing with median, categorical with mode
                for col in df_cleaned.columns:
                    if df_cleaned[col].isna().any():
                        if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                            df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
                        else:
                            mode_val = df_cleaned[col].mode()
                            if not mode_val.empty:
                                df_cleaned[col] = df_cleaned[col].fillna(mode_val.iloc[0])
                commit_action(df_cleaned)
                st.rerun()
    else:
        st.info("📂 Upload a dataset to get started")
        st.caption("Supported formats: " + ", ".join(SUPPORTED_FORMATS))

# ---------------------------------------------------------------------------
# 5. Main Dashboard View
# ---------------------------------------------------------------------------
if "df" in st.session_state:
    df = st.session_state["df"]
    kpi = calculate_kpi_metrics(df)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    all_cols = df.columns.tolist()
    
    # ---------------------------------------------------------------------------
    # 5a. KPI Cards (Executive Dashboard)
    # ---------------------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📊 Total Records</div>
            <div class="kpi-value">{kpi['Total Records']:,}</div>
            <div class="kpi-change neutral">Dataset Size</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📋 Data Completeness</div>
            <div class="kpi-value">{kpi['Completeness']:.1f}%</div>
            <div class="kpi-change {'positive' if kpi['Completeness'] > 90 else 'negative'}">
                {kpi['Missing Values']:,} missing values
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">🔍 Data Quality</div>
            <div class="kpi-value">{kpi['Duplicate Rows']:,}</div>
            <div class="kpi-change {'positive' if kpi['Duplicate Rows'] == 0 else 'negative'}">
                duplicate rows
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">📁 Data Structure</div>
            <div class="kpi-value">{kpi['Total Columns']}</div>
            <div class="kpi-change neutral">columns available</div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # 5b. Filter Bar (Interactive Dashboard)
    # ---------------------------------------------------------------------------
    st.markdown("""
    <div class="filter-bar">
        <div class="filter-group">
            <label>🔍 Filter:</label>
        </div>
    """, unsafe_allow_html=True)
    
    # Create dynamic filters
    filter_cols = st.columns([2, 2, 2, 1, 1])
    
    with filter_cols[0]:
        # Date filter if date columns exist
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        if date_cols:
            date_filter = st.selectbox("Date Column", [None] + date_cols)
            if date_filter:
                min_date = df[date_filter].min()
                max_date = df[date_filter].max()
                date_range = st.date_input("Date Range", [min_date, max_date])
    
    with filter_cols[1]:
        # Categorical filter
        if categorical_cols:
            cat_filter = st.selectbox("Category", [None] + categorical_cols)
            if cat_filter:
                unique_vals = df[cat_filter].unique().tolist()
                selected_vals = st.multiselect("Values", unique_vals, default=unique_vals[:5] if len(unique_vals) > 5 else unique_vals)
    
    with filter_cols[2]:
        # Numeric range filter
        if numeric_cols:
            num_filter = st.selectbox("Numeric Column", [None] + numeric_cols)
            if num_filter:
                min_val = float(df[num_filter].min())
                max_val = float(df[num_filter].max())
                range_vals = st.slider("Range", min_val, max_val, (min_val, max_val))
    
    with filter_cols[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Apply Filters", use_container_width=True):
            st.rerun()
    
    with filter_cols[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧹 Clear All", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # 5c. Main Dashboard Charts (2-column layout)
    # ---------------------------------------------------------------------------
    st.markdown("### 📈 Analytics Overview")
    
    chart_col1, chart_col2 = st.columns(2)
    
    # Left chart - Distribution or Bar chart
    with chart_col1:
        st.markdown("""
        <div class="chart-container">
            <div class="chart-header">
                <h3>Data Distribution</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if numeric_cols:
            selected_num = st.selectbox("Select column", numeric_cols, key="dist_col")
            fig = px.histogram(df, x=selected_num, 
                               title=f"Distribution of {selected_num}",
                               color_discrete_sequence=["#3B82F6"],
                               marginal="box")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(family="Inter"),
                            height=400)
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True, key="dist_chart")
        else:
            st.info("No numeric columns available for distribution chart")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Right chart - Categorical breakdown
    with chart_col2:
        st.markdown("""
        <div class="chart-container">
            <div class="chart-header">
                <h3>Category Breakdown</h3>
            </div>
        """, unsafe_allow_html=True)
        
        if categorical_cols:
            selected_cat = st.selectbox("Select category", categorical_cols, key="cat_col")
            cat_counts = df[selected_cat].value_counts().reset_index()
            cat_counts.columns = [selected_cat, 'count']
            
            fig = px.bar(cat_counts, x=selected_cat, y='count',
                        title=f"Distribution of {selected_cat}",
                        color_discrete_sequence=["#8B5CF6"],
                        text_auto=True)
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(family="Inter"),
                            height=400)
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True, key="cat_chart")
        else:
            st.info("No categorical columns available for breakdown chart")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------------
    # 5d. Bottom Row - Correlation/Scatter and Data Table
    # ---------------------------------------------------------------------------
    if len(numeric_cols) >= 2:
        st.markdown("### 🔬 Correlation Analysis")
        
        corr_cols = st.columns(2)
        
        with corr_cols[0]:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">
                    <h3>Scatter Plot</h3>
                </div>
            """, unsafe_allow_html=True)
            
            x_col = st.selectbox("X-Axis", numeric_cols, key="x_scatter")
            y_col = st.selectbox("Y-Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0, key="y_scatter")
            
            fig = px.scatter(df, x=x_col, y=y_col,
                           title=f"{x_col} vs {y_col}",
                           trendline="ols",
                           color_discrete_sequence=["#6366F1"])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(family="Inter"),
                            height=350)
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#F1F5F9')
            st.plotly_chart(fig, use_container_width=True, key="scatter_chart")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with corr_cols[1]:
            st.markdown("""
            <div class="chart-container">
                <div class="chart-header">
                    <h3>Correlation Matrix</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='Blues',
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False
            ))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(family="Inter"),
                            height=350,
                            xaxis=dict(side="bottom"),
                            yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, key="corr_chart")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ---------------------------------------------------------------------------
    # 5e. Data Preview with Export Options
    # ---------------------------------------------------------------------------
    st.markdown("### 📋 Data Preview")
    
    preview_tabs = st.tabs(["📊 Table View", "📈 Summary Stats", "📥 Export Data"])
    
    with preview_tabs[0]:
        # Show data with pagination
        rows_per_page = st.selectbox("Rows per page", [25, 50, 100, 200], index=1)
        total_pages = max(1, (len(df) + rows_per_page - 1) // rows_per_page)
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * rows_per_page
        end_idx = min(start_idx + rows_per_page, len(df))
        
        st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)
        st.caption(f"Showing rows {start_idx+1} to {end_idx} of {len(df):,}")
    
    with preview_tabs[1]:
        # Summary statistics
        st.markdown("#### Numerical Columns")
        if numeric_cols:
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)
        else:
            st.info("No numerical columns found")
        
        st.markdown("#### Categorical Columns")
        if categorical_cols:
            cat_stats = []
            for col in categorical_cols[:5]:  # Limit to avoid performance issues
                cat_stats.append({
                    "Column": col,
                    "Unique Values": df[col].nunique(),
                    "Most Common": df[col].mode().iloc[0] if not df[col].mode().empty else "N/A",
                    "Missing": df[col].isna().sum()
                })
            st.dataframe(pd.DataFrame(cat_stats), use_container_width=True)
        else:
            st.info("No categorical columns found")
    
    with preview_tabs[2]:
        st.markdown("#### Export Options")
        export_cols = st.columns(3)
        
        with export_cols[0]:
            st.download_button(
                "📥 Download CSV",
                df.to_csv(index=False).encode('utf-8'),
                file_name=f"insightiq_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_cols[1]:
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            st.download_button(
                "📥 Download Excel",
                buffer.getvalue(),
                file_name=f"insightiq_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with export_cols[2]:
            st.download_button(
                "📥 Download Summary",
                df.describe().to_csv().encode('utf-8'),
                file_name=f"insightiq_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    # ---------------------------------------------------------------------------
    # 5f. Data Quality Report
    # ---------------------------------------------------------------------------
    with st.expander("📊 Data Quality Report", expanded=False):
        quality_metrics = {
            "Metric": ["Total Rows", "Total Columns", "Missing Values", "Duplicate Rows", 
                      "Data Completeness", "Unique Values (avg)"],
            "Value": [
                f"{len(df):,}",
                f"{len(df.columns)}",
                f"{df.isna().sum().sum():,}",
                f"{df.duplicated().sum():,}",
                f"{(1 - df.isna().sum().sum() / (len(df) * len(df.columns))) * 100:.1f}%",
                f"{df.nunique().mean():.1f}"
            ]
        }
        st.dataframe(pd.DataFrame(quality_metrics), hide_index=True, use_container_width=True)
        
        # Column-by-column quality
        st.markdown("#### Column Details")
        col_quality = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Missing": df.isna().sum(),
            "Missing %": (df.isna().sum() / len(df) * 100).round(1),
            "Unique": df.nunique(),
            "Sample": df.iloc[0].values if len(df) > 0 else ["N/A"] * len(df.columns)
        })
        st.dataframe(col_quality, use_container_width=True)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center; padding: 80px 20px; background: white; border-radius: 16px; border: 2px dashed #E2E8F0; margin-top: 40px;">
        <div style="font-size: 64px; margin-bottom: 20px;">📊</div>
        <h2 style="font-size: 28px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">Executive Dashboard</h2>
        <p style="font-size: 18px; color: #475569; max-width: 500px; margin: 0 auto 24px;">
            Upload a dataset from the sidebar to unlock powerful analytics, 
            interactive visualizations, and data-driven insights.
        </p>
        <div style="display: flex; gap: 12px; justify-content: center;">
            <span style="padding: 6px 16px; background: #F1F5F9; border-radius: 999px; font-size: 13px; color: #475569;">CSV</span>
            <span style="padding: 6px 16px; background: #F1F5F9; border-radius: 999px; font-size: 13px; color: #475569;">Excel</span>
            <span style="padding: 6px 16px; background: #F1F5F9; border-radius: 999px; font-size: 13px; color: #475569;">JSON</span>
            <span style="padding: 6px 16px; background: #F1F5F9; border-radius: 999px; font-size: 13px; color: #475569;">Parquet</span>
            <span style="padding: 6px 16px; background: #F1F5F9; border-radius: 999px; font-size: 13px; color: #475569;">+ More</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; padding: 24px 0 16px; border-top: 1px solid #E2E8F0; margin-top: 32px;">
    <span style="font-size: 13px; color: #94A3B8; font-weight: 500;">
        InsightIQ Executive Dashboard v2.0 · Built with Streamlit & Plotly
    </span>
</div>
""", unsafe_allow_html=True)
