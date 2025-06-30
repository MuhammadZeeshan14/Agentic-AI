import os
import chainlit as cl

from agents import Agent, OpenAIChatCompletionsModel, Runner
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Step 1 Provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

# Step 2 Model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    tracing_disabled=True
)

# Step 3 Agent
agent = Agent(
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    name="support_agent",
    )

@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history",[])
    await cl.Message(content="Hello! I'm Support Agent, How may I help you.").send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history") or []
    
    history.append({"role":"user","content":message.content})
    result = await Runner.run(
        starting_agent=agent,
        input=message.content,
        run_config=config
    )
    history.append({"role":"assistant","content":result.final_output})
    cl.user_session.set("history",history)
    await cl.Message(content=result.final_output).send()