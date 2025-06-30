# Hello Chainlit

This project was created using the `uv` package manager in Windows Terminal and Cursor IDE.

## Project Creation

This Python package was initialized using the following command in Windows Terminal:

```bash
uv init --package hello_chainlit
```

The `uv init` command created the basic project structure including:
- `pyproject.toml` - Project configuration and metadata
- `src/hello_chainlit/` - Source code directory structure
- `src/hello_chainlit/__init__.py` - Main package file
- `README.md` - This documentation file
- `uv.lock` - Dependency lock file

## Adding Chainlit

After initializing the project, Chainlit was added as a dependency using the following command in Cursor terminal:

```bash
uv add chainlit
```

This command added Chainlit to the project dependencies in `pyproject.toml` and updated the `uv.lock` file.

## Creating the Chatbot

A Python file named `chatbot.py` was created in the `src/hello_chainlit/` directory with a simple Chainlit chatbot implementation:

```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # Our custom logic goes here...
    # Send a fake response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
```

## Running the Application

The Chainlit application can be run using the following command in Cursor terminal:

```bash
uv run chainlit run src/hello_chainlit/chatbot.py -w
```

The `-w` flag enables watch mode, which automatically reloads the application when code changes are made.

## What is uv?

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and virtualenv, offering significantly faster performance.

## What is Chainlit?

Chainlit is an open-source framework for building conversational AI applications. It provides a simple way to create chat interfaces for AI models and chatbots.

## Project Structure

```
hello_chainlit/
├── pyproject.toml         # Project configuration
├── README.md             # This file
├── uv.lock               # Dependency lock file
└── src/
    └── hello_chainlit/
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

3. Run the Chainlit application:
   ```bash
   uv run chainlit run src/hello_chainlit/chatbot.py -w
   ```

4. Open your browser and navigate to `http://localhost:8000` to start chatting with the bot.

## Development

This project uses modern Python packaging standards with `pyproject.toml` for configuration and `uv` for dependency management. The chatbot can be customized by modifying the `chatbot.py` file, and changes will automatically reload thanks to Chainlit's watch mode.
