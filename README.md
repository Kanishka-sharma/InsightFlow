# InsightFlow

**InsightFlow** is an AI-driven **Automated Exploratory Data Analysis (Auto-EDA)** tool powered by **Google Gemini**.  
It enables users to upload any CSV dataset and automatically performs data exploration, visualization, and summary generation - all within a streamlined **Streamlit** interface.

---

## Key Features

- **Upload CSV Files** - Instantly preview your dataset.
- **AI-Powered EDA Planning** - Gemini generates a step-by-step EDA plan and Python code.
- **Automated Execution** - Each step executes safely in an isolated Python environment.
- **Smart Visualizations** - Generates histograms, boxplots, and correlation heatmaps automatically.
- **Comprehensive Reports** - AI summarizes findings into a structured Markdown and downloadable PDF report.
- **Secure & Efficient** - Built with restricted execution and safe plotting for reliable operation.

---

## How It Works

1. **Upload** your dataset (CSV file).  
2. **Gemini** creates an intelligent EDA plan based on your analysis goal.  
3. The system **executes** the generated Python code cell by cell, capturing outputs and visualizations.  
4. **InsightFlow** compiles all results into a clear, concise, and professional **EDA report** ready for download.

---
## Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini 2.5 Flash |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Reporting** | ReportLab |
| **Environment Management** | Python-dotenv |



