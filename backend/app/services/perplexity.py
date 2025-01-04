import os
import json
import requests
from typing import List, Dict, Any


def generate_summary(query: str, focus_urls: List[str], context: str = None) -> str:
    """
    Отправляет запрос в Perplexity API для генерации саммари.

    Args:
        query: Текстовый запрос пользователя.
        focus_urls: Список URL-адресов веб-сайтов.
        context: Опциональный текстовый контекст.

    Returns:
        Текст саммари или сообщение об ошибке.
    """
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return "Error: PERPLEXITY_API_KEY not set in environment variables"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload: Dict[str, Any] = {
        "query": query,
        "focus": focus_urls
    }

    if context:
        payload["context"] = context

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            return response.json()["summary"]
        else:
            error_message = response.json().get("error", "Unknown error")
            return f"Error from Perplexity API: {error_message}"

    except requests.RequestException as e:
        return f"Error from Perplexity API: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from Perplexity API"
    except Exception as e:
        return f"Unexpected error: {str(e)}" 