"""
Utilities for LLM model management: download and return local model path.
"""
import os
from huggingface_hub import snapshot_download

# Environment variable pointing to the HuggingFace repo ID or local path of your LLM model
MODEL_REPO = os.getenv("HF_MODEL_ID", "google/gemma-3-1b-it")
# Optional: specify a directory to download the model into (default: "models")
LOCAL_DIR = os.getenv("HF_CACHE_DIR", "models")

def get_model_path():
    """
    Download the model from the HuggingFace Hub if not already present and return the local path.
    Uses HF_TOKEN environment variable for authentication to access gated models.
    Returns:
        str: path to the local model directory
    """
    import os
    
    # Get HF token from secrets or environment
    import streamlit as st
    hf_token = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_HUB_TOKEN")
    print(f"[llm_utils] HF_TOKEN found: {hf_token}")
    if not hf_token:
        print("Warning: No HF_TOKEN found. You may need to set it for access to gated models.")
        print("Try: export HF_TOKEN=your_token_here")
    
    # Download the model with token
    print(f"Downloading model: {MODEL_REPO}")
    path = snapshot_download(
        repo_id=MODEL_REPO, 
        local_dir=LOCAL_DIR,
        token=hf_token,
        ignore_patterns=["*.bin", "*.h5"]  # Only download model config and tokenizer initially
    )
    
    print(f"Model files downloaded to {path}")
    return path
