"""
Utilities for LLM model management: now supports Together API for LLM calls.
"""
import os
from together import Together

# SECURITY: Do NOT hardcode your API key! Set it as an environment variable: TOGETHER_API_KEY

def runner(prompt, model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"):
    """
    Calls the Together API for LLM chat completion.
    Args:
        prompt (str): The user prompt for the LLM.
        model (str): Together model name. Default: Llama-3 70B Turbo.
    Returns:
        str: The model's reply.
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable not set.")
    client = Together(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
