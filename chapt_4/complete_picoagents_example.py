
import asyncio
import os

from picoagents import Agent, OpenAIChatCompletionClient


def get_weather(location: str) -> str:
    """Get the weather for a given location"""
    return f"The weather in {location} is sunny"


# Create an agent
agent = Agent(
    name="Weather Agent",
    description="A agent that gets the weather for a given location",
    instructions="You are a weather agent that gets the weather for a given location",
    model_client=OpenAIChatCompletionClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1-mini",
    ),
    tools=[get_weather],
)   

async def run_agent():
    async for event in agent.run_stream("What is the weather in Tokyo?"):
        print(event)

if __name__ == "__main__":
    asyncio.run(run_agent())


