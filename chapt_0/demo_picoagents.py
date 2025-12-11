"""Demo of using picoagents to create a multi-agent system"""

import asyncio
import os

from picoagents import Agent
from picoagents.llm import OpenAIChatCompletionClient
from picoagents.orchestration import RoundRobinOrchestrator
from picoagents.termination import MaxMessageTermination, TextMentionTermination
from picoagents.webui import serve

# Ste up the language model
client = OpenAIChatCompletionClient(
    api_key=os.getenv('OPENAI_API_KEY'),
    model='gpt-4.1-mini',
)

# Create a Haiku poet
poet = Agent(
    name='Poet',
    description="Haiku poet.",
    instructions="You are a haiku poet. You are given a topic and you need to write a haiku about it.",
    model_client=client,
)


# Test the poet
async def test_poet():
    result = await poet.run("Write a haiku about the weather.")
    print(result)
    
    print(result.context.messages[-1].content)
    
    
# Add a critic agent
critic = Agent(
    name='Critic',
    description="POetry critic who provides constructive feedback on haiku poems.",
    instructions="You are a critic of haiku poems. When you see a haiku, provide 2 - 3 specific, actionable \
                    suggestions for improvement. Be constructive and brief. \
                    If satisfied with teh kaiku, respond with 'Approved'.", 
    model_client=client,
)

# Test the critic agent
async def test_critic():
    haiku = "Clouds drift soft and slow, \
              whispering winds touch the earth, \
              rain's gentle embrace."
    result = await critic.run(f"Please critique this haiku: {haiku}")
    print(result)
    
    print(result.context.messages[-1].content)
    
    
# Round Robin orchestration
termination = MaxMessageTermination(max_messages=8) | TextMentionTermination(text="APPROVED")
orchestrator = RoundRobinOrchestrator(agents=[poet, critic], termination=termination, max_iterations=4)

# Run orchestrator
async def run_orchestrator():
    task = "Write a haiku about cherry blossoms in Spring"
    stream = orchestrator.run_stream(task)
    
    
    async for message in stream:
        print(f"{message}")


if __name__ == "__main__":
    
    # asyncio.run(run_orchestrator())
    
    # Run the web ui    
    serve(entities=[orchestrator], port=8070, auto_open=True)
