import os
from dotenv import load_dotenv
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from tools.game_tools import roll_dice, generate_event

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Sub-agents 
narrator_agent = Agent(
    name="NarratorAgent",
    instructions="Narrate the story and describe what happens next.",
    model=model
)

monster_agent = Agent(
    name="MonsterAgent",
    instructions="Describe a monster encounter. Ask what the player wants to do in combat.",
    model=model
)

item_agent = Agent(
    name="ItemAgent",
    instructions="Describe treasure, magical items, and rewards. Let player decide how to use them.",
    model=model
)

# Main Game Master Agent
game_master_agent = Agent(
    name="GameMasterAgent",
    instructions="""
You are the Game Master of a text-based fantasy game. Guide the player.
Use tools like roll_dice() and generate_event().
Handoff to:
- NarratorAgent for story
- MonsterAgent for combat
- ItemAgent for loot
""",
    model=model,
    tools=[roll_dice, generate_event],
    handoffs=[
        handoff(agent=narrator_agent),
        handoff(agent=monster_agent),
        handoff(agent=item_agent)
    ]
)

@cl.on_chat_start
async def welcome():
    await cl.Message(content="🎮 Welcome to the Fantasy Adventure Game! Just type your action, like:\n- 'I enter the dungeon'\n- 'Roll a dice'\n- 'Attack the goblin'\nLet's begin your quest! ⚔️").send()

# Handling messages
@cl.on_message
async def handle_message(message: cl.Message):
    result = await Runner.run(game_master_agent, message.content)
    await cl.Message(content=result.final_output).send()
