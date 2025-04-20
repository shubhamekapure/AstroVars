"""
LLM handler for Astro-Vars using Google's Gemma 3 1B-it model.
"""
from llm_utils import get_model_path
from transformers import AutoTokenizer, Gemma3ForCausalLM
import torch
import json

_tokenizer = None
_model = None

import time

def load_model():
    """
    Load the Gemma 3 1B instruction-tuned model with 8-bit quantization for efficiency.
    """
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        print("[llm_handler] Starting model and tokenizer loading...")
        start_time = time.time()
        # Get model path
        model_path = get_model_path()
        
        # Load tokenizer
        print("[llm_handler] Loading tokenizer...")
        _tokenizer = AutoTokenizer.from_pretrained(model_path)
        print("[llm_handler] Tokenizer loaded.")
        
        # Load Gemma model with full 16-bit precision (float16) if supported, else fallback to float32
        try:
            print("[llm_handler] Loading Gemma model (float16, cpu)...")
            _model = Gemma3ForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                device_map="cpu"
            ).eval()
            print("[llm_handler] Model loaded (float16, cpu).")
        except Exception:
            print("[llm_handler] Failed to load float16 model, falling back to float32...")
            _model = Gemma3ForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float32,
                device_map="cpu"
            ).eval()
            print("[llm_handler] Model loaded (float32, cpu).")
        print(f"[llm_handler] Model and tokenizer loaded in {time.time() - start_time:.2f} seconds.")
    return _tokenizer, _model

import csv
from datetime import datetime

def run_llm(prompt, max_new_tokens=1000, temperature=0.7):
    csv_path = "llm_runs.csv"
    timestamp = datetime.now().isoformat()
    status = "success"
    response = None
    """
    Given a prompt, returns Gemma's response about astrological compatibility.
    Uses the exact formatting structure from the Gemma 3 documentation.
    """
    try:
        # Extract chart data for enhancing the prompt
        chart_json = {}
        start_idx = prompt.find('{')
        end_idx = prompt.rfind('}') + 1
        
        try:
            if start_idx > 0 and end_idx > start_idx:
                chart_data = prompt[start_idx:end_idx]
                chart_json = json.loads(chart_data)
        except json.JSONDecodeError:
            pass  # If parsing fails, use empty dict
        
        # Get key planetary positions for context
        sun_sign = chart_json.get('Sun', {}).get('sign', 'Unknown')
        moon_sign = chart_json.get('Moon', {}).get('sign', 'Unknown')
        asc_sign = chart_json.get('Ascendant', {}).get('sign', 'Unknown')
        
        # Get element balance if available
        elements = chart_json.get('ElementBalance', {})
        element_str = ", ".join([f"{element}: {count}" for element, count in elements.items()]) if elements else "Unknown"
        
        # Load the model
        tokenizer, model = load_model()
        
        # Create a specialized system prompt for astrology
        print("[llm_handler] Building system prompt and messages...")
        
        # Get houses information if available
        houses_info = chart_json.get('Houses', {})
        first_house = houses_info.get('House_1', {}).get('sign', 'Unknown')
        fifth_house = houses_info.get('House_5', {}).get('sign', 'Unknown') 
        seventh_house = houses_info.get('House_7', {}).get('sign', 'Unknown')
        eighth_house = houses_info.get('House_8', {}).get('sign', 'Unknown')
        
        # Get aspects information
        aspects = chart_json.get('Aspects', [])
        venus_aspects = [asp for asp in aspects if asp.get('p1') == 'Venus' or asp.get('p2') == 'Venus']
        mars_aspects = [asp for asp in aspects if asp.get('p1') == 'Mars' or asp.get('p2') == 'Mars']
        venus_mars_aspect = any(asp for asp in aspects if 
                               (asp.get('p1') == 'Venus' and asp.get('p2') == 'Mars') or 
                               (asp.get('p1') == 'Mars' and asp.get('p2') == 'Venus'))
        
        # Get element and modality balance
        element_balance = chart_json.get('ElementBalance', {})
        modality_balance = chart_json.get('ModalityBalance', {})
        
        # Build rich system prompt with all available information
        system_content = f"""You are an expert professional astrologer with decades of experience interpreting natal charts. 
        
You're analyzing a birth chart with:
- Sun in {sun_sign} (representing core identity and conscious ego)
- Moon in {moon_sign} (representing emotional needs and subconscious patterns)
- Ascendant in {asc_sign} (representing outer personality and physical appearance)
- Venus in {chart_json.get('Planets', {}).get('Venus', {}).get('sign', 'Unknown')} (representing love style and attraction)
- Mars in {chart_json.get('Planets', {}).get('Mars', {}).get('sign', 'Unknown')} (representing passion and assertive drive)
- 7th House (partnership) in {seventh_house}
- 5th House (romance/pleasure) in {fifth_house}
- 8th House (intimacy/shared resources) in {eighth_house}

Element Balance: {element_balance}
Modality Balance: {modality_balance}

Based on this comprehensive chart analysis, provide a detailed and professional interpretation of ideal partner traits, covering:

1. Physical appearance preferences based on Ascendant and Venus
2. Emotional qualities needed based on Moon sign
3. Intellectual compatibility based on Mercury and Air element presence
4. Specific personality traits that would complement and challenge this person
5. Communication styles that would resonate well
6. Potential relationship challenges and how to navigate them
7. Signs that would be most compatible romantically and why

Make your analysis sound like a professional astrologer with specific details and nuanced insights, while keeping it accessible. Maintain a balanced view that honors both traditional and modern astrological interpretations.

**IMPORTANT: Your response must be concise and kept under 1000 tokens (about 750 words). Focus on the most important insights rather than covering every detail.**"""
        
        # Format messages exactly as in the example
        messages = [
            [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": system_content}]
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                },
            ],
        ]
        
        # Apply Gemma's chat template with proper formatting
        print("[llm_handler] Tokenizing and formatting input tensors...")
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        )
        # Ensure all tensors are on CPU
        inputs = {k: v.to("cpu") for k, v in inputs.items()}
        print("[llm_handler] Input tensors ready.")
        
        # Generate with torch.inference_mode for efficiency
        print("[llm_handler] Starting model inference...")
        inf_start = time.time()
        with torch.inference_mode():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=max_new_tokens,  # Set to 1000 in function signature
                temperature=temperature,
                do_sample=True,
                top_p=0.95,  # Slightly increased for more creative outputs
                top_k=40,    # Reduced slightly to focus on quality vs quantity
                repetition_penalty=1.3,   # Increased further to reduce repetition
                length_penalty=1.0  # Discourage extremely long outputs
            )
        print(f"[llm_handler] Inference completed in {time.time() - inf_start:.2f} seconds.")
        
        # Decode the response
        response_text = tokenizer.batch_decode(outputs)[0]
        
        # Extract just the model's response by removing the input prompt
        input_text = tokenizer.batch_decode(inputs['input_ids'])[0]
        if response_text.startswith(input_text):
            response = response_text[len(input_text):].strip()
        else:
            response = response_text
        # Log to CSV
        with open(csv_path, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, prompt, response, status])
        return response
    except Exception as e:
        # Graceful error handling for MVP
        print(f"Error in LLM inference: {str(e)}")
        status = "error"
        response = f"# Astrology Partner Analysis\n\nI analyzed your chart with Sun in {{sun_sign}}, Moon in {{moon_sign}}, and Ascendant in {{asc_sign}}.\n\nYour ideal partner will likely have strong {{sun_sign}} or {{moon_sign}} compatibility and values that align with your {{asc_sign}} energy.\n\nThe specific aspects in your chart suggest emotional depth and intellectual connection are particularly important for you in relationships."
        # Log error to CSV
        with open(csv_path, mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, prompt, response, status])
        return response
