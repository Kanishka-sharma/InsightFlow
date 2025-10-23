import os
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import builtins
from types import SimpleNamespace
from utils import capture_stdout, unique_filename, format_exception

# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Allowed builtins for safe execution 
ALLOWED_BUILTINS = {
    "len", "min", "max", "sum", "abs", "round", "range",
    "enumerate", "sorted", "list", "dict", "set", "tuple", "print",
    "str", "int", "float", "bool", "type", "isinstance", "hasattr",
    "getattr", "setattr", "zip", "__import__"
}


class ExecutionResult(SimpleNamespace):
    """Container for execution results"""
  

def _make_safe_builtins():
    return {k: getattr(builtins, k) for k in ALLOWED_BUILTINS if hasattr(builtins, k)}


def execute_code_cells(code_cells, csv_path=None):
    """
    Executes a list of Python code cells (strings) in a shared namespace.
    Returns a list of ExecutionResult objects.
    """

    # Persistent namespace for all cells
    ns = {
        "pd": pd,
        "np": np,
        "plt": plt,
        "sns": sns,
    }
    ns["__builtins__"] = _make_safe_builtins()

    # Preload CSV into df 
    if csv_path:
        ns["__uploaded_csv__"] = csv_path
        try:
            ns["df"] = pd.read_csv(csv_path)
        except Exception as e:
            return [ExecutionResult(success=False, output="", error=f"Failed to load CSV: {e}", images=[])]

    results = []

    for idx, code in enumerate(code_cells, start=1):
        images = []
        try:
            # Capture stdout
            with capture_stdout() as buf:
                exec(code, ns)
                for num in plt.get_fignums():
                    fig = plt.figure(num)
                    fname = unique_filename(f"plot_cell_{idx}")
                    fig.savefig(fname, bbox_inches="tight")
                    images.append(fname)
                    plt.close(fig)

            output_text = buf.getvalue().strip()
            results.append(ExecutionResult(success=True, output=output_text, error=None, images=images))

        except Exception as e:
            results.append(ExecutionResult(
                success=False,
                output=buf.getvalue().strip() if "buf" in locals() else "",
                error=format_exception(e),
                images=images
            ))
            continue

    return results