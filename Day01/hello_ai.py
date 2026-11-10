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

# Send a request to the Ollama API
response = client.chat.completions.create(
    model=os.getenv("MODEL"),
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
)

# Display the response
print(response.choices[0].message.content)
