"""
Test script for Gemma 3 1B-it integration with HF token
"""
import os
import torch
from transformers import AutoTokenizer, Gemma3ForCausalLM
from transformers import logging

# Set logging to show only errors
logging.set_verbosity_error()

# Check for token
import streamlit as st
hf_token = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
if not hf_token:
    print("⚠️ No HF_TOKEN environment variable found!")
    print("Please set it with: export HF_TOKEN=your_token_here")
    exit(1)
else:
    print("✓ HF_TOKEN found")

# Model ID
model_id = "google/gemma-3-1b-it"
print(f"Testing model: {model_id}")

try:
    # Load tokenizer
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
    print("✓ Tokenizer loaded successfully")

    # Load model in 16-bit precision if supported, else fallback to float32
    print("Loading Gemma 3 model in 16-bit precision... (this may take a minute)")
    try:
        model = Gemma3ForCausalLM.from_pretrained(
            model_id,
            token=hf_token,
            torch_dtype=torch.float16,
            device_map="cpu"
        ).eval()
        print("✓ Model loaded successfully in float16!")
    except Exception:
        model = Gemma3ForCausalLM.from_pretrained(
            model_id,
            token=hf_token,
            torch_dtype=torch.float32,
            device_map="cpu"
        ).eval()
        print("✓ Model loaded successfully in float32!")
    
    # Test with astrology prompt
    # Use random but valid test input
    name = "Alexandra"
    dob = "1992-07-15"
    place = "Barcelona, Spain"
    system_content = f"You are an expert astrologer analyzing a birth chart for {name}, born on {dob} in {place}, with Sun in Taurus, Moon in Gemini, and Ascendant in Libra."
    user_prompt = "What are the ideal partner traits for this person? Keep it concise and insightful."
    # Format messages
    messages = [
        [
            {
                "role": "system",
                "content": [{"type": "text", "text": system_content}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}]
            },
        ],
    ]
    
    print("\nGenerating response...")
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    )
    # Ensure all tensors are on CPU
    inputs = {k: v.to("cpu") for k, v in inputs.items()}
    
    with torch.inference_mode():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True,
            top_p=0.9
        )
    
    # Extract model response
    response_text = tokenizer.batch_decode(outputs)[0]
    input_text = tokenizer.batch_decode(inputs['input_ids'])[0]
    if response_text.startswith(input_text):
        response = response_text[len(input_text):].strip()
    else:
        response = response_text
    
    print("\n===== GEMMA RESPONSE =====")
    print(response)
    print("==========================")
    
    print("\n✅ Test completed successfully! Your Astro-Vars app is ready to use Gemma.")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nTroubleshooting tips:")
    print("1. Make sure your HF_TOKEN is correct and you've accepted the model terms")
    print("2. Check your internet connection")
    print("3. Verify you have enough disk space and memory")
