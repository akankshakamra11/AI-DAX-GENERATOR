import os

from google import genai
from google.genai import types


class GeminiService:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash").strip()

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from the .env file.")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=8192,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
