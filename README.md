# MCP Expense Chat

A Streamlit chatbot that connects to an MCP expense tracker server using LangChain and GPT-5.

## Features

- Chat interface to query your expenses
- Connects to a remote MCP expense tracking server
- Powered by OpenAI GPT-5 with tool calling

## Setup

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Configure secrets

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "your_openai_api_key"
XAI_API_KEY = "your_xai_api_key"
horizon_api_key = "Bearer your_mcp_api_key"
expense_server_url = "https://your-mcp-server/mcp"
```

Or use a `.env` file (switch to `os.getenv` in `config.py`):
```
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_api_key
horizon_api_key=Bearer your_mcp_api_key
expense_server_url=https://your-mcp-server/mcp
```

### 3. Run the app
```
streamlit run app.py
```

## Project Structure

```
mcp_host/
├── app.py          # Streamlit chat UI
├── main.py         # MCP client + LLM logic
├── config.py       # API keys and config
├── requirements.txt
└── .gitignore
```
