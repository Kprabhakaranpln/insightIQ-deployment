# 🌌 InsightIQ | Data Refinery

**Data Refinery, Reimagined.**  
InsightIQ is a highly responsive, web-based data engineering and visual analytics engine built with Python and Streamlit. It allows users to upload raw datasets and instantly clean, transform, pivot, and visualize the information without writing a single line of code. 

Designed with a modern glassmorphism UI, it provides a seamless desktop and mobile analytics experience.

## 🚀 Live Demo
[**Click here to view the live app!**](https://insightiq-deployment-am4z2z2bvitnbmpxgydm56.streamlit.app)

---

## 🛠️ Key Features

- **⚡ Universal Import:** Natively supports 8 data formats including Big Data standards (`.csv`, `.xlsx`, `.xls`, `.json`, `.jsonl`, `.xml`, `.parquet`, `.avro`).
- **⏳ Pipeline Time-Travel (Undo/Redo):** Features a robust session-state memory that tracks your transformation history, allowing you to undo or redo data cleaning steps instantly.
- **🧬 Smart Cleaning:** One-click anomaly detection to remove duplicates and drop missing values. Advanced imputation handles corrupted text nulls (e.g., `"nane"`, `"null"`) and fills them via statistical methods (Mean, Median, Mode, or Zero).
- **⚙️ Data Transformation:** Easily isolate, drop, or rename dimensions (columns) to structure your payload perfectly.
- **🔀 Pivot Matrix Generator:** Group and aggregate your data on the fly. Create multiple custom pivot tables (Mean, Sum, Count, Max, Min) and visualize them instantly.
- **📈 Visual Analytics:** Generate dynamic, interactive Plotly charts (Bar, Line, Scatter, Pie, Histogram) or trigger the **Automated Dashboard** for an instant statistical overview (Density, Variance, Correlation).
- **💾 Final Export:** Download your processed, refined matrices directly to CSV or Excel payloads.

---

## 🤖 24/7 Keep-Awake Automation (Anti-Sleep Bot)

Streamlit Community Cloud automatically hibernates applications after 12 hours of inactivity. To ensure InsightIQ remains instantly accessible 24/7 without "cold-start" loading delays, this repository features a custom-engineered **Headless Browser Bot**.

### How the Bot Works:
Because Streamlit ignores standard HTTP background pings, the bot is designed to simulate a real human user session.
1. **The Script (`keep_awake.py`):** Uses **Playwright** to launch a headless Chromium browser in the background. It navigates to the live application URL, executes the JavaScript, and holds the active WebSocket connection open for 15 seconds.
2. **The Automation (`.github/workflows/keep_awake.yml`):** A GitHub Actions CI/CD pipeline triggers the Python script automatically every 10 hours. 
3. **The Result:** The Streamlit hosting server registers constant, valid user activity, preventing the container from ever going to sleep.

---

## 🏗️ Architecture & Tech Stack

- **Core Engine:** Python 3.11
- **Frontend Framework:** Streamlit (with custom CSS for mobile responsiveness & glassmorphism)
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly Express
- **I/O Dependencies:** `openpyxl`, `xlrd`, `fastavro`
- **Automation:** Playwright, GitHub Actions

---

## 💻 Local Installation

To run InsightIQ on your local machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/InsightIQ.git](https://github.com/your-username/InsightIQ.git)
   cd InsightIQ
