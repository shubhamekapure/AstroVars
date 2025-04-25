import os
from datetime import datetime

from llm_utils import run_llm



# --- Main terminal interaction ---
def main():
    print("=== AstroVars Terminal ===")
    name = input("Name: ")
    place = input("Place of Birth (City, Country): ")
    date = input("Date of Birth (YYYY-MM-DD): ")
    time = input("Time of Birth (HH:MM, 24hr): ")


    # Optionally, get LLM interpretation
    ask_llm = input("Would you like an AI interpretation of your birth details? (y/n): ").strip().lower()
    if ask_llm.startswith('y'):
        prompt = f"""
Name: {name}\nPlace of Birth: {place}\nDate of Birth: {date}\nTime of Birth: {time}\n\nPlease provide a detailed astrological interpretation and personality analysis based on these birth details. If you need to infer signs, do so from the information provided, and explain your reasoning clearly.\n"""
        print("\nGetting AI interpretation...")
        try:
            llm_output = run_llm(prompt)
            print("\n--- AI Interpretation ---\n")
            print(llm_output)
        except Exception as e:
            print(f"Error calling LLM: {e}")

if __name__ == "__main__":
    main()
