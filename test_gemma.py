"""
Test script for Gemma 3 1B-it model integration
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import logging
import sys

# Set logging to show only errors
logging.set_verbosity_error()

def test_gemma():
    print("Loading Gemma 3 1B-it model...")
    
    model_id = "google/gemma-3-1b-it"
    
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Load model with reduced precision for efficiency
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        low_cpu_mem_usage=True
    )
    
    print("Model loaded successfully!")
    
    # Create a test prompt related to astrology
    astro_prompt = """
    You are an expert astrologer. Analyze this birth chart with:
    - Sun in Aries
    - Moon in Pisces
    - Ascendant in Leo
    
    Provide a brief analysis of ideal partner traits for this person.
    """
    
    # Format using Gemma's chat template
    messages = [{"role": "user", "content": astro_prompt}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False)
    
    print("\nGenerating response...")
    
    # Tokenize input and generate response
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1
        )
    
    # Decode response
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract just the model's response
    if "<model>" in full_response:
        model_start = full_response.find("<model>") + len("<model>")
        model_end = full_response.find("</model>")
        if model_end > model_start:
            response = full_response[model_start:model_end].strip()
        else:
            response = full_response.replace("<model>", "").strip()
    else:
        response = full_response.replace(prompt, "").strip()
    
    print("\n===== RESPONSE =====")
    print(response)
    print("====================")
    
    return True

if __name__ == "__main__":
    try:
        print("Testing Gemma 3 1B-it integration...")
        success = test_gemma()
        if success:
            print("\nTest completed successfully! You can now run the full Astro-Vars app.")
            sys.exit(0)
    except Exception as e:
        print(f"\nError testing Gemma model: {str(e)}")
        sys.exit(1)
