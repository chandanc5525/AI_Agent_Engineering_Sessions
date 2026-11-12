"""Local tools used by the Day05 LangChain tool-calling agent.

The agent decides which tool to call, passes the arguments, reads the
observation returned by the tool, and then produces its final answer.

Every tool is a plain Python function decorated with ``@tool`` so LangChain
can expose its name, description, and argument schema to the model.
"""

from __future__ import annotations

import ast
import math
import operator
from datetime import datetime
from pathlib import Path

from langchain_core.tools import tool

# All file tools are sandboxed to this folder. The agent cannot read or write
# files outside ``Day05/workspace``.
WORKSPACE_DIR = Path(__file__).resolve().parent / "workspace"
WORKSPACE_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Calculator helpers
# ---------------------------------------------------------------------------

_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "sqrt": math.sqrt,
    "pow": pow,
}

_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _evaluate(node: ast.AST) -> float:
    """Safely evaluate a small arithmetic AST without using ``eval``."""
    if isinstance(node, ast.Expression):
        return _evaluate(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")

    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return operation(_evaluate(node.left), _evaluate(node.right))

    if isinstance(node, ast.UnaryOp):
        operation = _UNARY_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return operation(_evaluate(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ValueError("Unknown function. Allowed: " + ", ".join(_FUNCTIONS))
        if node.keywords:
            raise ValueError("Keyword arguments are not supported.")
        function = _FUNCTIONS[node.func.id]
        return function(*(_evaluate(argument) for argument in node.args))

    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def _resolve_workspace_path(filename: str) -> Path:
    """Return a path inside the workspace, blocking ``..`` traversal."""
    candidate = (WORKSPACE_DIR / filename).resolve()
    if candidate != WORKSPACE_DIR and WORKSPACE_DIR not in candidate.parents:
        raise ValueError(
            "Access denied. Files must stay inside the Day05/workspace folder."
        )
    return candidate


# ---------------------------------------------------------------------------
# Tools exposed to the agent
# ---------------------------------------------------------------------------


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression and return the result.

    Use this tool for every calculation instead of doing maths in your head.
    Supports +, -, *, /, //, %, **, parentheses, pi, e, abs, round, min, max,
    sum, sqrt, and pow. Example: ``(12 * 8) + sqrt(144)``.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _evaluate(parsed)
    except Exception as exc:  # noqa: BLE001 - report any bad input to the model
        return f"Calculator error: {exc}"

    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return f"{expression} = {result}"


@tool
def get_current_datetime(timezone: str = "local") -> str:
    """Return the current date and time.

    Use this tool whenever the user asks about today, the current time, or a
    date calculation. ``timezone`` can be ``local`` (default) or an IANA name
    such as ``Asia/Kolkata`` or ``UTC``.
    """
    try:
        if timezone.strip().lower() in ("", "local"):
            tz = datetime.now().astimezone().tzinfo
        else:
            from zoneinfo import ZoneInfo

            tz = ZoneInfo(timezone)

        now = datetime.now(tz)
    except Exception:
        return (
            f"Unknown timezone: {timezone}. "
            "Use 'local' or an IANA name such as 'Asia/Kolkata' or 'UTC'."
        )

    return now.strftime("%A, %d %B %Y, %I:%M:%S %p (%Z)")


@tool
def list_workspace_files() -> str:
    """List all files in the Day05 workspace folder.

    Use this tool before reading a file when you do not know its exact name.
    """
    files = sorted(
        path.relative_to(WORKSPACE_DIR).as_posix()
        for path in WORKSPACE_DIR.rglob("*")
        if path.is_file()
    )

    if not files:
        return "The workspace is empty."

    return "Files in the workspace:\n" + "\n".join(f"- {name}" for name in files)


@tool
def read_text_file(filename: str) -> str:
    """Read a UTF-8 text file from the Day05 workspace and return its contents.

    ``filename`` must be relative to the workspace, for example ``notes.txt``
    or ``reports/summary.md``. Paths outside the workspace are rejected.
    """
    try:
        path = _resolve_workspace_path(filename)
    except ValueError as exc:
        return str(exc)

    if not path.exists():
        return f"File not found: {filename}. Use list_workspace_files to see available files."
    if not path.is_file():
        return f"Not a file: {filename}"

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"Cannot read {filename}: it is not a UTF-8 text file."
    except OSError as exc:
        return f"Cannot read {filename}: {exc}"

    if len(content) > 20_000:
        content = content[:20_000] + "\n\n... [file truncated at 20,000 characters]"

    return f"Contents of {filename}:\n{content}"


@tool
def write_text_file(filename: str, content: str) -> str:
    """Create or overwrite a UTF-8 text file inside the Day05 workspace.

    ``filename`` must be relative to the workspace, for example ``notes.txt``.
    Use this tool when the user asks you to save, create, or update a file.
    Always tell the user the filename after saving.
    """
    try:
        path = _resolve_workspace_path(filename)
    except ValueError as exc:
        return str(exc)

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        return f"Cannot write {filename}: {exc}"

    return f"Saved {len(content)} characters to {filename}."


@tool
def word_count(text: str) -> str:
    """Count the words, characters, and lines in a piece of text.

    Use this tool when the user asks for text statistics. Pass the full text
    you want to analyse as the ``text`` argument.
    """
    words = len(text.split())
    characters = len(text)
    characters_without_spaces = len("".join(text.split()))
    lines = len(text.splitlines()) or 1

    return (
        f"Words: {words}\n"
        f"Characters: {characters}\n"
        f"Characters (without spaces): {characters_without_spaces}\n"
        f"Lines: {lines}"
    )


# The order here is also the order shown in the CLI and the Streamlit sidebar.
TOOLS = [
    calculator,
    get_current_datetime,
    list_workspace_files,
    read_text_file,
    write_text_file,
    word_count,
]
