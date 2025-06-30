# OpenAI Agents Project

This project was created using the `uv` package manager in Windows Terminal.

## Project Creation

This Python project was initialized using the following command in Windows Terminal:

```bash
uv init test
```

The `uv init` command created the basic project structure including:
- `pyproject.toml` - Project configuration and metadata
- `main.py` - Main application file
- `README.md` - This documentation file
- `uv.lock` - Dependency lock file

After opening the project in Cursor IDE, we added the OpenAI agents packages using:

```bash
uv add openai-agents
```

## What is uv?

`uv` is a fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and virtualenv, offering significantly faster performance.

## Project Structure

```
test/
├── pyproject.toml         # Project configuration
├── main.py               # Main application file
├── README.md             # This file
├── uv.lock               # Dependency lock file
└── src/
    └── openai_agents/
        └── __init__.py   # Main package code
```

## Getting Started

To work with this project:

1. Install uv if you haven't already:
   ```bash
   pip install uv
   ```

2. Install the project in development mode:
   ```bash
   uv sync
   ```

3. Run the project:
   ```bash
   uv run python main.py
   ```

## Development

This project uses modern Python packaging standards with `pyproject.toml` for configuration and `uv` for dependency management. The OpenAI agents packages were added using the `uv add openai-agents` command for enhanced AI capabilities.
