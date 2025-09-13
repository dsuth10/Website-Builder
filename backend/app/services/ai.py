from __future__ import annotations
import httpx
from ..core.config import get_settings


class AIClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = self.settings.openrouter_model
        self.api_key = self.settings.openrouter_api_key

    async def generate_html(self, title: str, topic: str, reading_level: str) -> str:
        if not self.api_key:
            # Fallback content when key not set; helps local dev without secrets
            return f"<h1>{title}</h1><p>Topic: {topic}</p><p>Reading level: {reading_level}</p><p>(Provide OPENROUTER_API_KEY to enable generation.)</p>"

        system = (
            "You are an assistant generating kid-friendly website content. "
            "Write clear, concise, factual content. Produce semantic HTML only. "
            "No scripts or styles. Headings, paragraphs, lists are okay."
        )
        user = (
            f"Title: {title}\n"
            f"Topic: {topic}\n"
            f"Reading level target: {reading_level}.\n"
            "Return only HTML body (no <html> or <head>)."
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://example.local",
            "X-Title": "School Site Generator",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.7,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"].strip()
            return content

