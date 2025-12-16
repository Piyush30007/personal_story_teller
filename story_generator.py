from dotenv import load_dotenv
from google import genai
from gtts import gTTS
from io import BytesIO
import os

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


# ---------- PROMPT CREATION ----------
def create_advanced_prompt(style: str) -> str:
    base_prompt = f"""
**Your Persona:** You are a friendly and engaging storyteller.
**Your Main Goal:** Write a story in simple, clear, and modern English.
**Your Task:** Create ONE single story that connects all the provided images in order.
**Style Requirement:** The story must fit the '{style}' genre.

**Core Instructions:**
1. Tell one complete story (beginning, middle, end).
2. Use a key detail from every image.
3. Creatively infer relationships between images.
4. Use ONLY Indian names, characters, places, and settings.

**Output Format:**
- Title at the top
- 4 to 5 paragraphs
"""

    style_instruction = ""

    if style == "Morale":
        style_instruction = (
            "\n[MORAL]: Add a single-sentence moral at the end."
        )
    elif style == "Mystery":
        style_instruction = (
            "\n[SOLUTION]: Reveal the culprit and the key clue."
        )
    elif style == "Thriller":
        style_instruction = (
            "\n[TWIST]: Reveal a shocking final twist."
        )

    return base_prompt + style_instruction


# ---------- STORY GENERATION ----------
def generate_story_from_images(images: list, style: str) -> str:
    """
    images: list of image Parts (already prepared)
    style: story style
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=images + [create_advanced_prompt(style)]  # FIXED
    )

    return response.text


# ---------- TEXT TO SPEECH ----------
def narrate_story(story_text: str) -> BytesIO:
    """
    Converts story text to audio and returns a BytesIO object
    """

    try:
        tts = gTTS(text=story_text, lang="en", slow=False)
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp

    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {e}")
