from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv(override=True)

client = OpenAI(
    base_url=os.getenv("NVIDIA_BASE_URL"),
    api_key=os.getenv("NVIDIA_API_KEY")
)

response = client.chat.completions.create(
    model="meta/llama-3.1-8b-instruct",
    messages=[{"role": "user", "content": "Say hello in one sentence"}]
)

print(response.choices[0].message.content)