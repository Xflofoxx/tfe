
import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")

    def chat(self, model: str, prompt: str) -> str | None:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            resp = requests.post(url, json=payload, timeout=120)
            if resp.status_code != 200:
                return None
            data = resp.json()
            return data.get("response", "")
        except Exception as e:
            print(f"Ollama error: {e}")
            return None
