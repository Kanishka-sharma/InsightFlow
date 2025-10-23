import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from agent import plan_and_generate_code, extract_code_cells, summarize_report
from executor import execute_code_cells

# Load environment variables
load_dotenv()

# --- Streamlit page setup ---
st.set_page_config(page_title="Auto-EDA Agent", layout="wide")
st.title("🤖 Auto-EDA Agent")
st.write("Upload a CSV dataset and let the AI automatically explore, visualize, and summarize it for you!")

# --- Sidebar configuration ---
st.sidebar.header("⚙️ Configuration")
goal = st.sidebar.text_area(
    "Analysis Goal (optional)", placeholder="Example: Find key factors influencing churn"
)
run_button = st.sidebar.button("🚀 Run Auto EDA")

# --- Ensure directories exist ---
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# --- File uploader ---
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    # Save uploaded file
    csv_path = os.path.join("uploads", uploaded_file.name)
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    # Preview uploaded data
    df = pd.read_csv(csv_path)
    st.write("### 🧾 Preview of Uploaded Data")
    st.dataframe(df.head())

    if run_button:
        # --- Step 1: Generate EDA plan from Gemini ---
        with st.spinner("🤖 Thinking... generating EDA plan..."):
            plan_markdown = plan_and_generate_code(goal or "General EDA", csv_path)

        st.markdown("### 🧠 EDA Plan")
        st.markdown(plan_markdown)

        # --- Step 2: Extract code blocks ---
        code_cells = extract_code_cells(plan_markdown)
        st.write(f"🔍 Found {len(code_cells)} code blocks to execute.")

        # --- Step 3: Execute code cells ---
        all_outputs = []
        all_images = []

        for i, code in enumerate(code_cells, 1):
            st.markdown(f"---\n### 🧩 Step {i}")
            st.code(code, language="python")

            with st.spinner(f"Running step {i}..."):
                results = execute_code_cells([code], csv_path=csv_path)
                for result in results:
                    if result.success:
                        if result.output:
                            st.text_area("🧾 Output", result.output, height=150)
                        if result.images:
                            for img_path in result.images:
                                st.image(img_path, use_container_width=True)
                                all_images.append(img_path)
                    else:
                        st.error(f"⚠️ Error: {result.error}")

                    summary_text = f"Step {i} Output:\n{result.output}\n\nError: {result.error}\n"
                    all_outputs.append(summary_text)

        # --- Step 4: Summarize EDA into report ---
        with st.spinner("📊 Summarizing results into final EDA report..."):
            full_summary_text = "\n".join(all_outputs)
            report_md = summarize_report(goal or "General EDA", plan_markdown, full_summary_text)

        st.markdown("---")
        st.markdown("## 🧾 Final EDA Report")
        st.markdown(report_md)

        # --- Step 5: Offer report for download as a Markdown file ---
        st.download_button(
            label="💾 Download Report (.md)",
            data=report_md,
            file_name="auto_eda_report.md",
            mime="text/markdown",
        )

else:
    st.info("👆 Upload a CSV file to get started.")