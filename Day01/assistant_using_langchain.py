import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Load Configuration from .env file
load_dotenv()

# Initialize the ChatOllama model using the environment variable
# (LangChain's ChatOllama natively picks up or accepts the model configured in your .env)
model_name = os.getenv("MODEL", "qwen3:1.7b")
base_url = os.getenv("BASE_URL", "http://localhost:11434")

# Create the LangChain Ollama chat model client
# Note: ChatOllama can connect directly via base_url if needed, or defaults to localhost:11434
llm = ChatOllama(
    model=model_name,
    base_url=base_url
)

print('*' * 40)
print('My LangChain Ollama Assistant')
print('*' * 40)

while True:
    # Get user input
    user_input = input("\nEnter your question (or type 'exit' to quit): ")

    # Exit the loop if the user types 'exit'
    if user_input.lower() == 'exit':
        print("Exiting the assistant. Goodbye!")
        break

    # Wrap the user input in LangChain's HumanMessage abstraction
    messages = [HumanMessage(content=user_input)]

    # Invoke the model
    response = llm.invoke(messages)

    # Display the response content
    print("\nAI Response:")
    print(response.content)