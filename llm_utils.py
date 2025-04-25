"""
Utilities for LLM model management: now supports Together API for LLM calls.
"""
import os
from together import Together

# SECURITY: Do NOT hardcode your API key! Set it as an environment variable: TOGETHER_API_KEY

def runner(prompt, model="meta-llama/Llama-4-Scout-17B-16E-Instruct", temperature=1, max_tokens=700, top_p=0.9):
    """
    Calls the Together API for LLM chat completion.
    Args:
        prompt (str): The user prompt for the LLM.
        model (str): Together model name. Default: Llama-3 70B Turbo.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum tokens in the response.
        top_p (float): Nucleus sampling probability.
    Returns:
        str: The model's reply.
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY environment variable not set.")
    client = Together(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message.content.strip()

