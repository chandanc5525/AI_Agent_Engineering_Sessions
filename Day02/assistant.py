from openai import OpenAI
from dotenv import load_dotenv
import os


# Load Configuration from .env file
load_dotenv()

# Create a client that connects to the Ollama API
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

print('*'*40)
print('My Ollama API Configuration Assistant')
print('*'*40)

message = []

while True:
    # Get user input
    user_input = input("\nEnter your question (or type 'exit' to quit): ")

    # Save the user input to the message list
    message.append({"role": "user", 
                    "content": user_input})

    # Exit the loop if the user types 'exit'
    if user_input.lower() == 'exit':
        print("Exiting the assistant. Goodbye!")
        break

    # Send a request to the Ollama API
    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages = message
    )

    # Display the response
    print("\nAI Response:")
    print(response.choices[0].message.content)