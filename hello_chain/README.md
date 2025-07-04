# Hello Chain

This project was created using the `uv` package manager in Windows Terminal and Cursor IDE.

## Project Creation

This Python package was initialized using the following command in Windows Terminal:

```bash
uv init --package hello_chain
```

The `uv init` command created the basic project structure including:
- `pyproject.toml` - Project configuration and metadata
- `src/hello_chain/` - Source code directory structure
- `src/hello_chain/__init__.py` - Main package file
- `README.md` - This documentation file
- `uv.lock` - Dependency lock file

## Adding Dependencies

After initializing the project, the following dependencies were added using the Cursor terminal:

```bash
uv add chainlit
uv add openai-agents
```

These commands added Chainlit and openai-agents to the project dependencies in `pyproject.toml` and updated the `uv.lock` file.

## Creating the Chatbot

A Python file named `chatbot.py` was created in the `src/hello_chain/` directory. This implementation uses the Gemini API (via OpenAI-compatible endpoints) and the openai-agents library to provide an agent-based conversational assistant. The chatbot maintains chat history, streams responses token by token, and uses environment variables for API keys.

Example implementation:

```python
import os
from dotenv import load_dotenv
import chainlit as cl
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.run import RunConfig

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    config = RunConfig(model=model, tracing_disabled=True)
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    cl.user_session.set("agent", agent)
    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})
    msg = cl.Message(content="")
    await msg.send()
    agent = cl.user_session.get("agent")
    config = cl.user_session.get("config")
    try:
        result = Runner.run_streamed(agent, history, run_config=config)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                token = event.data.delta
                await msg.stream_token(token)
        history.append({"role": "assistant", "content": msg.content})
        cl.user_session.set("chat_history", history)
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
```

## Running the Application

The Chainlit application can be run using the following command in Cursor terminal:

```bash
uv run chainlit run src/hello_chain/chatbot.py -w
```

The `-w` flag enables watch mode, which automatically reloads the application when code changes are made.

## What is uv?

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and virtualenv, offering significantly faster performance.

## What is Chainlit?

Chainlit is an open-source framework for building conversational AI applications. It provides a simple way to create chat interfaces for AI models and chatbots.

## What is openai-agents?

`openai-agents` is a library for building agent-based conversational AI applications, supporting OpenAI-compatible models and advanced agent orchestration.

## Project Structure

```
hello_chain/
├── pyproject.toml         # Project configuration
├── README.md             # This file
├── uv.lock               # Dependency lock file
└── src/
    └── hello_chain/
        ├── __init__.py   # Main package code
        └── chatbot.py    # Chainlit chatbot implementation
```

## Getting Started

To work with this project:

1. Install uv if you haven't already:
   ```bash
   pip install uv
   ```

2. Install the project dependencies:
   ```bash
   uv sync
   ```

3. Set up your environment variables:
   - Create a `.env` file in the project root with the following content:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```

4. Run the Chainlit application:
   ```bash
   uv run chainlit run src/hello_chain/chatbot.py -w
   ```

5. Open your browser and navigate to `http://localhost:8000` to start chatting with the bot.

## Development

This project uses modern Python packaging standards with `pyproject.toml` for configuration and `uv` for dependency management. The chatbot can be customized by modifying the `chatbot.py` file, and changes will automatically reload thanks to Chainlit's watch mode.
