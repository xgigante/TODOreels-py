import os

import httpx

LM_STUDIO_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1")
MODEL = os.environ.get("AI_MODEL", "qwen3.8-27b-mlx")


async def ask_llm(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{LM_STUDIO_URL}/chat/completions",
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            },
        )
        response.raise_for_status()
        data = response.json()
    return data["choices"][0]["message"]["content"]