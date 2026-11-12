"""Day05 - LangChain tool-calling agent (Streamlit version).

The agent can call local tools (calculator, date/time, workspace files, text
statistics) and use their results to answer the user.

Run from the Day05 folder:

    uv run streamlit run app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_openai import ChatOpenAI

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from tools import TOOLS  # noqa: E402  (import after sys.path update)

# Load Day05/.env explicitly, even when Streamlit starts from the repo root.
load_dotenv(BASE_DIR / ".env")

# ---------------------------------------------------------------------------
# Model configuration
# ---------------------------------------------------------------------------

model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv("BASE_URL", "http://localhost:11434/v1")
api_key = os.getenv("API_KEY", "ollama")

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


@st.cache_resource
def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        temperature=0.3,
    )


def build_agent(role: str):
    """Create a fresh agent for the selected role."""
    system_prompt = f"{ROLES[role]}\n\n{TOOL_GUIDANCE}"
    return create_agent(
        model=get_llm(),
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


def render_assistant_step(message) -> None:
    """Render the tool calls and/or text of one AI message."""
    for call in message.tool_calls:
        st.caption(f"🔧 Calling tool: `{call['name']}` with `{call['args']}`")

    text = message_text(message.content)
    if text:
        st.markdown(text)


def render_tool_result(message: ToolMessage) -> None:
    with st.expander(f"🔧 Tool result · {message.name}"):
        st.code(message_text(message.content), language="text")


# ---------------------------------------------------------------------------
# Streamlit page
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Day05 - LangChain Tool Agent",
    page_icon="🛠️",
    layout="centered",
)

st.title("🛠️ Day05 - LangChain Tool Agent")
st.caption("Powered by LangChain + Ollama + local tools")

with st.sidebar:
    st.header("Agent Settings")

    selected_role = st.selectbox(
        "Select Assistant Role",
        options=list(ROLES.keys()),
        format_func=lambda key: ROLE_NAMES[key],
    )

    st.write("Selected Role:", ROLE_NAMES[selected_role])
    st.write("Model:", model_name)

    with st.expander("Available tools"):
        for tool in TOOLS:
            first_line = (tool.description or "").strip().splitlines()[0]
            st.markdown(f"**{tool.name}**  \n{first_line}")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------------------------------------------------------
# Conversation state
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_role" not in st.session_state:
    st.session_state.selected_role = selected_role

# Reset the conversation when the role changes.
if st.session_state.selected_role != selected_role:
    st.session_state.messages = []
    st.session_state.selected_role = selected_role

# ---------------------------------------------------------------------------
# Render conversation history
# ---------------------------------------------------------------------------

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message_text(message.content))

    elif isinstance(message, AIMessage):
        if message.tool_calls or message_text(message.content):
            with st.chat_message("assistant"):
                render_assistant_step(message)

    elif isinstance(message, ToolMessage):
        render_tool_result(message)

# ---------------------------------------------------------------------------
# Handle new user input
# ---------------------------------------------------------------------------

user_input = st.chat_input("Ask me anything, or give me a task...")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # Remember which messages were already on screen. Anything new after the
    # agent runs is a tool call, tool result, or final answer.
    known_ids = {id(message) for message in st.session_state.messages}

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking and using tools..."):
            try:
                agent = build_agent(selected_role)

                # The agent runs the loop: model -> tool -> model -> answer.
                result = agent.invoke({"messages": st.session_state.messages})
                all_messages = [
                    message
                    for message in result["messages"]
                    if not isinstance(message, SystemMessage)
                ]

                for message in all_messages:
                    if id(message) in known_ids:
                        continue
                    if isinstance(message, AIMessage):
                        render_assistant_step(message)
                    elif isinstance(message, ToolMessage):
                        render_tool_result(message)

                st.session_state.messages = all_messages

            except Exception as exc:  # noqa: BLE001 - keep the UI alive
                st.error(f"Error: {exc}")
                st.session_state.messages.pop()  # remove the failed user message
