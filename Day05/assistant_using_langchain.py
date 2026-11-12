"""Day05 - LangChain tool-calling agent (terminal version).

This is the Day04 assistant upgraded into an agent. The model is given real
tools, decides which tool (if any) is needed, observes the result, and then
writes the final answer.

Run from the Day05 folder:

    uv run python assistant_using_langchain.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

# Make sure ``tools.py`` can be imported even when the script is launched from
# another directory (for example ``python Day05/assistant_using_langchain.py``).
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from tools import TOOLS  # noqa: E402  (import after sys.path update)

# Load Day05/.env explicitly, no matter which directory the script runs from.
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------

model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv("BASE_URL", "http://localhost:11434/v1")
api_key = os.getenv("API_KEY", "ollama")

llm = ChatOpenAI(
    model=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.3,
)

# ---------------------------------------------------------------------------
# Roles and agent instructions
# ---------------------------------------------------------------------------

ROLES = {
    "1": (
        "You are a friendly assistant. Explain concepts with simple examples "
        "and provide code snippets when necessary."
    ),
    "2": (
        "You are a concise assistant. Give short, direct answers and provide "
        "code snippets only when they add value."
    ),
    "3": (
        "You are a detailed assistant. Give thorough explanations with "
        "examples and code snippets when necessary."
    ),
    "4": (
        "You are a step-by-step assistant. Break every task into clear steps "
        "with examples and code snippets when necessary."
    ),
}

ROLE_NAMES = {
    "1": "Friendly Assistant",
    "2": "Concise Assistant",
    "3": "Detailed Assistant",
    "4": "Step-by-Step Assistant",
}

TOOL_GUIDANCE = """
You are a tool-using agent. Follow these rules:

1. Use the calculator tool for every arithmetic operation instead of guessing.
2. Use get_current_datetime for the current date or time.
3. Use list_workspace_files, read_text_file, and write_text_file when the user
   asks about files. File access is limited to the Day05/workspace folder.
4. Use word_count for text statistics.
5. If no tool is needed, answer directly without calling one.
6. Base your final answer on the tool observations. If a tool returns an error,
   explain the problem and suggest a fix.
7. Never claim that a file was saved or a calculation was done unless the
   matching tool actually returned a successful result.
"""


def build_agent(role: str):
    """Create a fresh agent for the selected role."""
    system_prompt = f"{ROLES[role]}\n\n{TOOL_GUIDANCE}"
    return create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=system_prompt,
        name="day05_tool_agent",
    )


def message_text(content) -> str:
    """Convert LangChain message content (string or content blocks) to text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(part for part in parts if part).strip()

    return str(content)


def print_tool_menu() -> None:
    print("\nAvailable tools:")
    for tool in TOOLS:
        first_line = (tool.description or "").strip().splitlines()[0]
        print(f"  - {tool.name}: {first_line}")


def print_message(message) -> None:
    """Print one agent message, including tool calls and tool results."""
    if isinstance(message, HumanMessage):
        print("\nYou:", message_text(message.content))

    elif isinstance(message, AIMessage):
        for call in message.tool_calls:
            print(f"\n[Tool call] {call['name']}({call['args']})")

        text = message_text(message.content)
        if text:
            print("\nAI:", text)

    elif isinstance(message, ToolMessage):
        print(f"\n[Tool result: {message.name}]\n{message_text(message.content)}")


def print_history(messages) -> None:
    print("\n" + "=" * 50)
    print("CONVERSATION HISTORY")
    print("=" * 50)

    for message in messages:
        print_message(message)

    print("\n" + "=" * 50)


def print_new_messages(messages, known_ids) -> None:
    """Print only messages produced during the latest agent invocation."""
    for message in messages:
        if isinstance(message, SystemMessage) or id(message) in known_ids:
            continue
        print_message(message)


def main() -> None:
    print("*" * 50)
    print("Day05 - LangChain Tool Agent")
    print("*" * 50)
    print(f"Model: {model_name}")
    print(f"Tools: {', '.join(tool.name for tool in TOOLS)}")

    print("\nSelect a role for the assistant:")
    for key, value in ROLE_NAMES.items():
        print(f"{key}. {value}")

    selected_role = input("\nEnter the number of your preferred role: ").strip()
    if selected_role not in ROLES:
        print("Invalid selection. Using default role.")
        selected_role = "1"

    print(f"\nSelected Role: {ROLE_NAMES[selected_role]}")
    print("\nCommands:")
    print("  exit / quit  - stop the assistant")
    print("  clear        - clear the conversation")
    print("  history      - show the conversation so far")
    print("  tools        - list the available tools")

    agent = build_agent(selected_role)

    # Conversation state. The system prompt is supplied by ``create_agent``,
    # so only human/AI/tool messages are stored here.
    messages = []

    while True:
        user_input = input("\nYou: ").strip()

        if not user_input:
            continue

        command = user_input.lower()

        if command in ("exit", "quit"):
            print("Exiting the agent. Goodbye!")
            break

        if command == "clear":
            messages = []
            print("Conversation cleared.")
            continue

        if command == "history":
            if messages:
                print_history(messages)
            else:
                print("The conversation is empty.")
            continue

        if command == "tools":
            print_tool_menu()
            continue

        messages.append(HumanMessage(content=user_input))
        known_ids = {id(message) for message in messages}

        try:
            # The agent runs the loop: model -> tool -> model ... -> final answer.
            result = agent.invoke({"messages": messages})
            all_messages = result["messages"]

            print_new_messages(all_messages, known_ids)

            # Keep the full conversation (without the injected system prompt)
            # so the next turn has complete context, including tool results.
            messages = [
                message
                for message in all_messages
                if not isinstance(message, SystemMessage)
            ]

        except Exception as exc:  # noqa: BLE001 - keep the CLI alive on errors
            print(f"\nError: {exc}")
            messages.pop()  # remove the failed user message


if __name__ == "__main__":
    main()
