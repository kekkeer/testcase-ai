# services/deepseek_client.py

from openai import OpenAI
import os

_client = None   # 👈 全局唯一

def get_client():
    global _client

    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    return _client