
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

# Load Configuration
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Initialize Chat Model
model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv("BASE_URL", "http://localhost:11434/v1")
api_key = os.getenv("API_KEY", "ollama")

llm = ChatOpenAI(
    model=model_name,
    base_url=base_url,
    api_key=api_key,
    temperature=0.7
)

# System Message
system_message = SystemMessage(
    content="You are a helpful assistant. Explain every concept with simple examples and provide code snippets when necessary."
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Application Title
st.title("🤖 My LangChain Ollama Assistant")
st.caption("Powered by LangChain + Ollama + Streamlit")

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.write(f"Model: {model_name}")

    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

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

                response = llm.invoke(
                    [system_message] + st.session_state.messages
                )

                ai_response = response.content

                st.markdown(ai_response)

                # Save AI Response
                st.session_state.messages.append(
                    AIMessage(content=ai_response)
                )

            except Exception as e:

                st.error(f"Error: {e}")

                # Remove failed user message
                st.session_state.messages.pop()
