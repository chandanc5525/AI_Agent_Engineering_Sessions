
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

print("*" * 40)
print("My LangChain Ollama Assistant")
print("*" * 40)

# Saving conversation messages
message = [
    SystemMessage(
        content="You are a helpful assistant. Explain every concept with simple examples and provide code snippets when necessary."
    )
]

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Exiting the assistant. Goodbye!")
        break

    # Append user input
    message.append(HumanMessage(content=user_input))

    # Invoke model with conversation history
    try:
        response = llm.invoke(message)

        # Append AI response
        message.append(AIMessage(content=response.content))

        # Display AI response
        print("\nAI:", response.content)

        # Display complete conversation history
        print("\n" + "=" * 40)
        print("CONVERSATION HISTORY")
        print("=" * 40)

        for msg in message:

            if isinstance(msg, HumanMessage):
                print("\nYou:", msg.content)

            elif isinstance(msg, AIMessage):
                print("\nAI:", msg.content)

        print("=" * 40)

    except Exception as e:
        print("\nError:", e)
