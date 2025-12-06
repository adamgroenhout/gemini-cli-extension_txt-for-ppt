import sys
import re

def verify_ppt_format(filepath):
    """
    Verifies that a text file follows the specific format for PowerPoint import.
    """
    try:
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return False

    # Check for empty file
    if not content_bytes:
        print("Warning: File is empty.")
        return True

    # 1. Check for CRLF line endings (mostly relevant for the raw bytes)
    # Note: Python's 'rb' mode reads raw bytes. We can check if \r\n is used generally,
    # but mixed line endings might be an issue.
    # However, strict check:
    if b'\n' in content_bytes and b'\r\n' not in content_bytes:
         print("Warning: File seems to use LF instead of CRLF. PowerPoint requires CRLF for best compatibility, though some versions might handle LF.")
         # We won't fail hard on this unless strict mode, but let's note it.

    try:
        content_str = content_bytes.decode('utf-8')
    except UnicodeDecodeError:
        print("Error: File is not valid UTF-8.")
        return False

    lines = content_str.splitlines(keepends=True) # Keep ends to verify \r\n individually if needed

    errors = []

    # Check for Markdown code blocks
    if "```" in content_str:
        errors.append("Output contains Markdown code blocks (```).")

    for i, line_raw in enumerate(lines):
        line_num = i + 1
        line = line_raw.rstrip('\r\n')

        # Skip empty lines? PowerPoint might ignore them or treat them as blank slides/points.
        # But usually we want continuous text.
        if not line:
            continue

        # Check indentation
        # Regex to capture leading whitespace
        match = re.match(r'^(\s*)', line)
        leading_ws = match.group(1) if match else ""

        # Check if leading whitespace contains spaces
        if ' ' in leading_ws:
             errors.append(f"Line {line_num}: Indentation contains spaces. Only tabs (\\t) are allowed.")

        # It's hard to distinguish a Slide Title from a Bullet Point just by looking at one line
        # without context, but the rule is:
        # No indent = Slide Title
        # 1+ tabs = Bullet Point

        # If it has indentation, it must be tabs.
        # If it has no indentation, it's a title.

        # We already checked for spaces. So if it's strictly tabs or empty, it matches the structure.

    if errors:
        print("Verification Failed:")
        for e in errors:
            print(f"- {e}")
        return False
    else:
        print("Verification Passed: Format is correct.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_format.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    success = verify_ppt_format(filepath)
    if not success:
        sys.exit(1)
