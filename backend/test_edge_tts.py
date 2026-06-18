import asyncio
import edge_tts

TEXT = """
Welcome to Podcast Buddy.

Today we are discussing the latest developments in Artificial Intelligence.

Researchers are making breakthroughs in voice cloning, autonomous agents, and AI-powered software development.

Stay tuned as we break down everything in simple terms.
"""

VOICE = "en-US-AndrewNeural"


async def main():
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save("test.mp3")
    print("Audio saved as test.mp3")


asyncio.run(main())