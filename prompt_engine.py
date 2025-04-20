"""
Prompt engine for Astro-Vars: builds prompts for the LLM from chart JSON and user info.
"""
import json

def build_prompt(chart_json, user_info):
    """
    Builds the prompt for the LLM.
    chart_json: dict of full natal chart
    user_info: dict with user context (name, gender, etc)
    Returns: prompt string
    """
    prompt = f"""
You are a professional astrologer with 20+ years of experience. Avoid generic horoscope style. Provide sourced, psychological and karmic reasoning.

User info:
{json.dumps(user_info, indent=2)}

Full Natal Chart (JSON):
{json.dumps(chart_json, indent=2)}

Based on this chart, what are the key traits the user should seek in a life partner?

Return sections: Ideal Emotional Traits, Ideal Physical/Behavioral Traits, Key Synastry Indicators, Partner Red Flags. Use markdown for formatting.
"""
    return prompt
