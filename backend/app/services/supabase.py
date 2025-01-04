import os
from typing import Dict, Any
from supabase import Client, create_client


def init_supabase_client() -> Client:
    """
    Инициализирует клиент Supabase используя переменные окружения.

    Returns:
        Client: Инициализированный клиент Supabase.

    Raises:
        Exception: Если не установлены необходимые переменные окружения.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_API_KEY")

    if not url or not key:
        raise Exception(
            "Необходимо установить переменные окружения SUPABASE_URL и SUPABASE_API_KEY"
        )

    return create_client(url, key)


def save_query_log(query: str, response: str, timestamp: str, client: Client) -> Dict[str, Any]:
    """
    Сохраняет лог запроса в Supabase.

    Args:
        query: Запрос пользователя.
        response: Ответ от Perplexity API.
        timestamp: Временная метка.
        client: Клиент Supabase.

    Returns:
        Dict[str, Any]: Результат операции вставки.

    Raises:
        Exception: При ошибке сохранения данных.
    """
    try:
        result = client.table("query_logs").insert({
            "query": query,
            "response": response,
            "timestamp": timestamp
        }).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        raise Exception(f"Ошибка при сохранении лога запроса: {str(e)}")


def get_query_log_by_id(query_id: int, client: Client) -> Dict[str, Any]:
    """
    Получает запись лога по ID.

    Args:
        query_id: ID записи для поиска.
        client: Клиент Supabase.

    Returns:
        Dict[str, Any]: Найденная запись или пустой словарь.

    Raises:
        Exception: При ошибке получения данных.
    """
    try:
        result = client.table("query_logs").select("*").eq("id", query_id).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        raise Exception(f"Ошибка при получении лога запроса: {str(e)}") 