import os
import uuid
import io
import contextlib
import traceback

# Directory to store generated plots and output artifacts
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def unique_filename(prefix: str, ext: str = ".png") -> str:
    """
    Generate a unique filename with a given prefix and extension.
    Example: outputs/figure_9f3a7b3e4b1.png
    """
    return os.path.join(OUTPUT_DIR, f"{prefix}_{uuid.uuid4().hex}{ext}")


@contextlib.contextmanager
def capture_stdout():
    """
    Capture print() statements inside a 'with' block.
    Example:
        with capture_stdout() as buffer:
            print("Hello")
        output = buffer.getvalue()
    """
    buffer = io.StringIO()
    old_stdout = None
    try:
        import sys
        old_stdout = sys.stdout
        sys.stdout = buffer
        yield buffer
    finally:
        if old_stdout is not None:
            import sys
            sys.stdout = old_stdout


def format_exception(e: Exception) -> str:
    """
    Return a clean one-line string representation of an exception.
    """
    return "".join(traceback.format_exception_only(type(e), e)).strip()
