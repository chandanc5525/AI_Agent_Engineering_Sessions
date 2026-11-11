
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

# Load Configuration from .env file
load_dotenv()

# Initialize the Chat Model
model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv("BASE_URL", "http://localhost:11434/v1")
api_key = os.getenv("API_KEY", "ollama")

# Create the LangChain Chat Model Client
llm = ChatOpenAI(
    model=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.7
)

# Streamlit Page Configuration
st.set_page_config(
    page_title="My LangChain Ollama Assistant",
    page_icon="🤖",
    layout="centered"
)

# Application Title
st.title("My LangChain Ollama Assistant")
st.caption("Powered by LangChain + Ollama")

# Define different roles for the assistant
roles = {
    "1": "You are a helpful assistant. Explain every concept with simple examples and provide code snippets when necessary.",
    "2": "You are a helpful assistant. Provide concise answers with code snippets when necessary.",
    "3": "You are a helpful assistant. Provide detailed explanations with examples and code snippets when necessary.",
    "4": "You are a helpful assistant. Provide step-by-step explanations with examples and code snippets when necessary."
}

# Define role names
role_names = {
    "1": "Friendly Assistant",
    "2": "Concise Assistant",
    "3": "Detailed Assistant",
    "4": "Step-by-Step Assistant"
}

# Sidebar Configuration
with st.sidebar:

    st.header("Assistant Settings")

    selected_role = st.selectbox(
        "Select Assistant Role",
        options=list(roles.keys()),
        format_func=lambda x: role_names[x]
    )

    st.write("Selected Role:", role_names[selected_role])

    st.write("Model:", model_name)

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_role" not in st.session_state:
    st.session_state.selected_role = selected_role

# Reset conversation when role changes
if st.session_state.selected_role != selected_role:

    st.session_state.messages = []
    st.session_state.selected_role = selected_role

# Define System Message
system_message = SystemMessage(
    content=roles[selected_role]
)

# Display Conversation History
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):

        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):

        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User Input
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Append User Message
    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    # Generate AI Response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                # Invoke model with conversation history
                response = llm.invoke(
                    [system_message] + st.session_state.messages
                )

                # Append AI Response
                st.session_state.messages.append(
                    AIMessage(content=response.content)
                )

                # Display AI Response
                st.markdown(response.content)

            except Exception as e:

                st.error(f"Error: {e}")

                # Remove failed user message
                st.session_state.messages.pop()
