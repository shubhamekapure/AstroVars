"""
LLM handler for AstroVars: sends user birth details to Together API LLM for interpretation.
"""
from llm_utils import run_llm

        print(f"[llm_handler] Model and tokenizer loaded in {time.time() - start_time:.2f} seconds.")
    return _tokenizer, _model

import csv
from datetime import datetime

from llm_utils import run_llm

def run_llm(name, date_of_birth, time_of_birth, place_of_birth):
    """
    Calls the Together API LLM for astrological interpretation focused on ideal partner traits.
    Args:
        name (str): Person's name
        date_of_birth (str): Date of birth (YYYY-MM-DD)
        time_of_birth (str): Time of birth (HH:MM)
        place_of_birth (str): Place of birth (city, country)
    Returns:
        str: LLM's astrological interpretation
    """
    prompt = (
        f"You are a world-class Vedic astrologer and relationship advisor.\n\n"
        f"Client Details:\n"
        f"Name: {name}\n"
        f"Date of Birth: {date_of_birth}\n"
        f"Time of Birth: {time_of_birth}\n"
        f"Place of Birth: {place_of_birth}\n\n"
        f"Using this information, analyze the client's birth chart and provide a detailed prediction of their ideal life partner.\n"
        f"Keep the response under 750 words.\n\n"
        f"Please structure your response as follows:\n\n"
        f"1. **Personality Overview** – Describe the individual's core traits, nature, and emotional tendencies based on their birth chart.\n"
        f"2. **Love & Relationship Tendencies** – How they behave in relationships, romantic needs, and challenges.\n"
        f"3. **Ideal Partner Traits** – The qualities they need in a life partner for a fulfilling relationship. Include zodiac compatibility if relevant.\n"
        f"4. **Astrological Houses & Planets** – Mention significant astrological indicators like Venus, 7th house, Moon sign, or ascendant.\n"
        f"5. **Advice for Lasting Love** – Give personalized advice to help them attract and sustain a healthy relationship.\n\n"
        f"Make it personalized, emotionally engaging, and insightful — like a professional astrology session."
    )
    return run_llm(prompt)
