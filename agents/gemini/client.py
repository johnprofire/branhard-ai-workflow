import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

API_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent"
)


class GeminiAgent:
    def __init__(self, role="general"):
        self.role = role

    def run(self, prompt, system_prompt=None):
        if not API_KEY:
            raise RuntimeError("GEMINI_API_KEY is missing from .env")

        instructions = prompt

        if system_prompt:
            instructions = (
                f"{system_prompt}\n\n"
                f"User request:\n{prompt}"
            )

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": instructions
                        }
                    ]
                }
            ]
        }

        headers = {
            "x-goog-api-key": API_KEY,
            "Content-Type": "application/json",
        }

        last_error = None

        for attempt in range(3):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    json=payload,
                    timeout=(15, 120)
                )

                if not response.ok:
                    raise RuntimeError(
                        f"Gemini API error {response.status_code}: "
                        f"{response.text}"
                    )

                data = response.json()

                return data["candidates"][0]["content"]["parts"][0]["text"]

            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.Timeout
            ) as error:
                last_error = error

                if attempt < 2:
                    print(
                        f"Gemini connection failed. "
                        f"Retrying ({attempt + 2}/3)..."
                    )
                    time.sleep(3)

        raise RuntimeError(
            f"Gemini connection failed after 3 attempts: {last_error}"
        )


def create_agent(role="general"):
    return GeminiAgent(role=role)
