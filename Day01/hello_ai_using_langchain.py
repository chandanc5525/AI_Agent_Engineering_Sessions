# Referecen Material: https://docs.langchain.com/oss/python/integrations/chat/ollama
from langchain.messages import HumanMessage
from langchain_ollama import ChatOllama



llm = ChatOllama(model="qwen3:1.7b", temperature=0)

# Send a message to Qwen
response = llm.invoke(
    [
        HumanMessage(
            content="What is the capital of India?"
        )
    ]
)

# Display response
print("\nAI Response:")
print(response.content)