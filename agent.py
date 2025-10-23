import os
import re
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env automatically if not already loaded
load_dotenv()

# Load Gemini API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment. Please set it in your .env file.")

# Configure Gemini client
genai.configure(api_key=GOOGLE_API_KEY)

# Default model
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# Prompt templates
PLAN_PROMPT = """
You are an expert data scientist and Python programmer.

Given a CSV dataset path and an analysis goal, create a numbered plan
for an Exploratory Data Analysis (EDA). For each step, provide:

1 A short title and purpose  
2 A runnable Python code block (```python ...   ``` ). Each import statement must be on its own line.

The code will be executed in an environment with:
- pandas (pd)
- numpy (np)
- matplotlib (plt)
- seaborn (sns)
- A variable __uploaded_csv__ that contains the path to the uploaded CSV file.

Return ONLY the plan and code blocks in markdown format. Do not include explanations outside of steps.
"""


SUMMARY_PROMPT = """
You are an expert data analyst. Based on the provided plan, goal, and outputs,
write a clean, professional Markdown EDA report.

Your report should include:
- Dataset overview (rows, columns, missing values)
- Key statistical insights
- Visual analysis with image references (use Markdown `![](path)` syntax)
- Correlation or feature relationships
- Final summary and recommendations

Be concise and professional. Assume this report will be read by business stakeholders.
"""


# Utility regex for extracting code blocks
CODE_BLOCK_RE = re.compile(r"```python\s*(.*?)```", re.DOTALL | re.IGNORECASE)


def call_gemini(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.2) -> str:
    """
    Calls Gemini with a given prompt and returns text output.
    """
    try:
        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(
            prompt,
            generation_config={"temperature": temperature},
        )
        return response.text.strip() if response.text else " No response received."
    except Exception as e:
        return f" Gemini API Error: {e}"


def plan_and_generate_code(goal: str, csv_path: str) -> str:
    """
    Ask Gemini to generate an EDA plan and code blocks.
    """
    user_prompt = f"""
{PLAN_PROMPT}

CSV path: {csv_path}
Analysis goal: {goal}
"""
    print("🤖 Generating EDA plan...")
    return call_gemini(user_prompt, model=DEFAULT_MODEL, temperature=0.2)


def extract_code_cells(plan_markdown: str) -> List[str]:
    """
    Extract all Python code blocks from Gemini's markdown output.
    """
    cells = CODE_BLOCK_RE.findall(plan_markdown)
    if not cells:
        print("⚠️ No code blocks found in Gemini output.")
    else:
        print(f" Extracted {len(cells)} code blocks.")
    return [c.strip() for c in cells]

def summarize_report(goal: str, plan_markdown: str, execution_summary: str) -> str:
    """
    Ask Gemini to summarize the plan and outputs into a Markdown EDA report.
    """
    user_prompt = f"""
{SUMMARY_PROMPT}

Analysis goal:
{goal}

EDA plan:
{plan_markdown}

Execution results:
{execution_summary}
    """
    print("🧠 Summarizing results...")
    return call_gemini(user_prompt, model=DEFAULT_MODEL, temperature=0.3)
