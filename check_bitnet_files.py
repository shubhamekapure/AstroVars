"""
Check what files are available in the BitNet repo
"""
from huggingface_hub import list_repo_files

# List all files in the model repository
files = list_repo_files("microsoft/bitnet-b1.58-2B-4T")
print("Files in the repository:")
for file in files:
    print(f"- {file}")
