# AI Agent Engineering Sessions
### *A Practical Journey into Generative AI, LLM Engineering & Autonomous AI Agents*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-purple?style=for-the-badge&logo=astral&logoColor=white)](https://astral.sh/uv)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/)
[![Qwen](https://img.shields.io/badge/Qwen-3%3A1.7b-orange?style=for-the-badge)](https://huggingface.co/Qwen)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Workflows-3399FF?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

---

## 📌 Executive Summary

**AI Agent Engineering Sessions** is a structured, hands-on engineering repository dedicated to learning, experimenting, and building intelligent AI applications. It covers the end-to-end journey from interacting with base Large Language Models (LLMs) to engineering tool-enabled autonomous agents, Retrieval-Augmented Generation (RAG) pipelines, and stateful multi-agent systems.

The ecosystem emphasizes **local-first execution**, leveraging `uv` for ultra-fast dependency isolation, `Ollama` for local model serving, `Qwen` as the primary open-weight LLM, and `LangChain` / `LangGraph` for orchestrating complex agentic workflows.

---

## 🛠️ Technology Stack

| Technology | Role & Category | Purpose |
| :--- | :--- | :--- |
| **Python** | Language | Core runtime (3.10+) |
| **uv** | Package Manager | Fast Python virtual environment and dependency lock management |
| **Ollama** | Local LLM Server | Local model execution engine and OpenAI-compatible REST server |
| **Qwen 3 (1.7B)** | Foundation Model | Primary open-weight language model for inference and tool calling |
| **OpenAI SDK** | API Client | Client library used to interface with Ollama’s OpenAI-compatible `/v1` endpoint |
| **LangChain** | Framework | Standardized abstractions for models, prompts, tools, and chains (LCEL) |
| **LangGraph** | Framework | Cyclic, stateful graph orchestrator for multi-agent workflows and persistence |
| **Python-dotenv**| Configuration | Environment-based configuration management for secure local settings |

---

## Create .env file

```
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL=qwen3:1.7b
```

## Run Version v1 LLM Chat Assistant Model

```
(AI_Agent_Engineering_Sessions) C:\AI_Agent_Engineering_Sessions\Day01>uv run streamlit run app.py
```
