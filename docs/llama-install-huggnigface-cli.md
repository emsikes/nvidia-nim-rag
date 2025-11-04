Step 1: Install Download Tools
bash# Install aria2 for robust downloads
sudo apt update
sudo apt install aria2 -y

# Make sure HuggingFace CLI is updated
pip install -U huggingface_hub

Step 2: Set Your HuggingFace Token
bash# Login to HuggingFace
huggingface-cli login
# Paste your HF token when prompted

# Or export it
export HF_TOKEN="hf_your_token_here"
Verify you accepted the license:
Visit: https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct

Step 3: Pre-download Model with Resume Support
This downloads the model separately with better error handling:
bash# Pre-download Llama 3.1 8B to cache
huggingface-cli download meta-llama/Meta-Llama-3.1-8B-Instruct \
  --resume-download \
  --cache-dir ~/.cache/huggingface
This will:

Download ~16GB in chunks
Auto-resume if interrupted
Show progress
Store in cache for vLLM to use


Step 4: Start vLLM (After Download Completes)
Once the download finishes:
bashpython -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --port 8001 \
  --gpu-memory-utilization 0.8 \
  --dtype auto \
  --api-key token-abc123
vLLM will find the model in the cache and won't need to download again.

Step 5: Monitor Progress
In another terminal, watch the download:
bash# Watch cache directory size
watch -n 5 du -sh ~/.cache/huggingface