import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = os.getenv(
    "DEEPSEEK_API_URL",
    "https://api.deepseek.com/chat/completions"
)
MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-flash")


class DeepSeekAgent:
    def __init__(self, role="general"):
        self.role = role

    def run(self, prompt, system_prompt=None):
        if not API_KEY:
            raise RuntimeError(
                "DEEPSEEK_API_KEY is missing from .env"
            )

        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        payload = {
            "model": MODEL,
            "messages": messages,
            "thinking": {
                "type": "enabled"
            }
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]


def create_agent(role="general"):
    return DeepSeekAgent(role=role)
