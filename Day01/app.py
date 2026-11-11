
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# 1. Load Environment Configuration
load_dotenv(override=True)

model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv(
    "BASE_URL",
    "http://localhost:11434/v1"
)
api_key = os.getenv("API_KEY", "ollama")

# 2. Streamlit Configuration
st.set_page_config(
    page_title="LLM Assistant:V1",
    page_icon="🤖",
    layout="centered"
)

st.title("LLM Assistant Chat Model: v1")
st.markdown('---')
st.header("Designed By: Chandan Chaudhari")
st.caption(f"Running model: {model_name}")

# 3. Initialize ChatOpenAI
@st.cache_resource
def load_model():

    llm = ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        temperature=0.7
    )

    return llm
# Create the LangChain Ollama chat model client
llm = load_model()

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input

user_input = st.chat_input("Ask me anything...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Convert chat history
    chat_history = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            chat_history.append(
                HumanMessage(content=message["content"])
            )

        else:
            chat_history.append(
                AIMessage(content=message["content"])
            )

# 7. Invoke Model
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = llm.invoke(chat_history)

                ai_response = response.content

                st.markdown(ai_response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_response
                })

            except Exception as e:

                st.error(f"Error connecting to Ollama: {e}")

# 8. Clear Chat
if st.sidebar.button("Clear Chat"):

    st.session_state.messages = []
    st.rerun()

# 9. Sidebar Configuration
st.sidebar.subheader("Model Configuration")
st.sidebar.write(f"Model: {model_name}")
st.sidebar.write(f"Base URL: {base_url}")
st.sidebar.success("OpenAI Compatible API")
