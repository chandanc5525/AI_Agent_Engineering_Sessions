🤖 AI Agent Engineering Sessions

A hands-on Python learning journey focused on building AI applications and intelligent agents using modern AI engineering tools and frameworks.

This project uses uv for Python project and dependency management, Ollama for running local LLMs, Qwen as the language model, and LangChain / LangGraph for developing AI applications and agents.

🚀 Technology Stack
Technology	Purpose
Python	Primary programming language
uv	Python package and project manager
Ollama	Run AI models locally
Qwen	Local Large Language Model (LLM)
OpenAI SDK	Connect to OpenAI-compatible APIs
LangChain	Build LLM applications and chains
LangGraph	Build stateful AI agent workflows
python-dotenv	Manage environment variables
📋 Prerequisites

Before starting, install:

Python 3.10 or later
uv
Ollama
Git (recommended)

Useful links:

Python
uv Documentation
Ollama
Qwen Models
LangChain Documentation
📁 Project Structure
text
AI_Agent_Engineering_Sessions/
│
├── .venv/
│
├── Day01/
│   ├── hello_ai.py
│   ├── hello_langchain.py
│   └── tool_calling.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md

⚙️ Project Setup
1. Clone the Repository
powershell
git clone <YOUR_REPOSITORY_URL>
cd AI_Agent_Engineering_Sessions


If you already created the project locally, simply navigate to its directory.

2. Install uv

Open PowerShell:

powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"


Verify installation:

powershell
uv --version

3. Initialize the Project

For a new project:

powershell
uv init --app


For an existing project with pyproject.toml, skip this step.

4. Create Virtual Environment
powershell
uv venv
.venv\Scripts\activate

5. Install Dependencies
powershell
uv add openai python-dotenv langchain langchain-ollama

🦙 Ollama Setup
1. Install Ollama

Download and install Ollama for Windows:

https://ollama.com/download/windows

2. Download Qwen Model

This project uses Qwen3 1.7B:

powershell
ollama pull qwen3:1.7b

3. Verify Model Installation
powershell
ollama list

4. Run Qwen
powershell
ollama run qwen3:1.7b


Ollama runs a local API at:

text
http://localhost:11434


OpenAI-compatible API endpoint:

text
http://localhost:11434/v1

🔐 Environment Configuration

Create a .env file in the project root:

env
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL=qwen3:1.7b


Configuration details:

BASE_URL: Ollama API endpoint.
API_KEY: Placeholder for the OpenAI-compatible SDK.
MODEL: Local Qwen model name.

Note: The LangChain ChatOllama integration can connect directly to Ollama without these OpenAI-compatible settings.

Never commit your .env file to Git.

📚 Day 01 – Getting Started with LLMs
Exercise 1: OpenAI SDK with Ollama

File: Day01/hello_ai.py

Learn how to connect a Python application to a locally running Qwen model using the OpenAI-compatible API.

Run:

powershell
uv run python Day01/hello_ai.py

Exercise 2: LangChain with Ollama

File: Day01/hello_langchain.py

Learn how to invoke a local Qwen model using LangChain's ChatOllama integration.

Run:

powershell
uv run python Day01/hello_langchain.py

Exercise 3: Tool Calling

File: Day01/tool_calling.py

Learn how to give an LLM access to Python functions and external tools.

Topics:

Defining tools using @tool
Binding tools to an LLM
Handling tool calls
Executing Python functions
Passing tool results back to the model

Run:

powershell
uv run python Day01/tool_calling.py

🧠 Learning Roadmap
Day	Topic	Learning Objective
Day 01	LLM Fundamentals	Understand and invoke LLMs
Day 02	Prompt Engineering	Design effective prompts
Day 03	LangChain	Build LLM applications
Day 04	Tool Calling	Enable LLMs to use tools
Day 05	Structured Output	Generate structured responses
Day 06	Embeddings	Understand vector representations
Day 07	RAG	Build document-based AI applications
Day 08	Vector Databases	Store and retrieve embeddings
Day 09	LangGraph	Build stateful AI agents
Day 10	Multi-Agent Systems	Coordinate multiple AI agents
🛠️ Useful Commands
Command	Description
uv init	Initialize Python project
uv venv	Create virtual environment
uv add package_name	Install dependency
uv remove package_name	Remove dependency
uv sync	Synchronize dependencies
uv run python file.py	Run Python application
uv tree	View dependency tree
uv lock	Update dependency lockfile
ollama list	List installed AI models
ollama pull qwen3:1.7b	Download Qwen
ollama run qwen3:1.7b	Run Qwen locally
🔒 Git Configuration

Add the following to .gitignore:

gitignore
# Virtual environment
.venv/

# Environment variables
.env
.env.*

# Python cache
__pycache__/
*.py[cod]

# IDE settings
.vscode/

# OS files
.DS_Store
Thumbs.db


Keep pyproject.toml and uv.lock in Git so other developers can reproduce the project environment.

🎯 Project Goals

By completing these sessions, the goal is to learn how to:

Work with locally hosted LLMs.
Build Python applications powered by AI.
Develop reusable prompt templates.
Implement tool calling.
Generate structured AI responses.
Build Retrieval-Augmented Generation (RAG) applications.
Work with vector databases.
Create intelligent AI agents.
Develop multi-agent systems using LangGraph.
📖 Learning Philosophy

Learn → Build → Experiment → Improve

Each session focuses on practical implementation rather than just theoretical concepts.

👨‍💻 Author

AI Agent Engineering Sessions

A practical learning journey into Generative AI, LLM Engineering, and Autonomous AI Agents.

⭐ If you find this project useful, feel free to star the repository and follow along with the learning journey.