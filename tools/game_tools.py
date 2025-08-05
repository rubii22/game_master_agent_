from agents.tool import function_tool
import random

@function_tool("roll_dice")
def roll_dice(sides: int = 6) -> str:
    """
    Simulates a dice roll and returns the result.
    """
    result = random.randint(1, sides)
    return f"🎲 You rolled a {result} on a {sides}-sided die."

@function_tool("generate_event")
def generate_event(location: str) -> str:
    """
    Generates a random fantasy event based on the location.
    """
    events = [
        f"A wild goblin jumps out from the shadows in {location}!",
        f"You discover a glowing chest buried in {location}.",
        f"A mysterious traveler offers you a quest in {location}.",
        f"You fall into a hidden trap in {location}!",
        f"The ground shakes beneath your feet in {location}!"
    ]
    return random.choice(events)
