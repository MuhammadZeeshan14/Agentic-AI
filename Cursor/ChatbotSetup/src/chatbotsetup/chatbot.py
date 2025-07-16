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