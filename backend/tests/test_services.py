import os
from typing import List
import pytest
import requests_mock
from backend.app.services.perplexity import generate_summary


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Фикстура для установки переменных окружения для тестов.
    """
    monkeypatch.setenv("PERPLEXITY_API_KEY", "test_api_key")


def test_generate_summary_success(mock_env_vars: None, requests_mock: requests_mock.Mocker) -> None:
    """
    Тест успешной генерации саммари через Perplexity API.
    """
    # Подготовка тестовых данных
    test_query = "Test query"
    test_urls = ["http://test.com"]
    expected_summary = "Test summary"
    
    # Мокирование ответа API
    requests_mock.post(
        "https://api.perplexity.ai/chat/completions",
        json={"summary": expected_summary}
    )
    
    # Выполнение теста
    result = generate_summary(test_query, test_urls)
    
    # Проверка результата
    assert result == expected_summary
    
    # Проверка правильности отправленного запроса
    last_request = requests_mock.last_request
    assert last_request.headers["Authorization"] == "Bearer test_api_key"
    assert last_request.json() == {
        "query": test_query,
        "focus": test_urls
    }


def test_generate_summary_with_context(mock_env_vars: None, requests_mock: requests_mock.Mocker) -> None:
    """
    Тест генерации саммари с дополнительным контекстом.
    """
    test_query = "Test query"
    test_urls = ["http://test.com"]
    test_context = "Previous context"
    expected_summary = "Test summary with context"
    
    requests_mock.post(
        "https://api.perplexity.ai/chat/completions",
        json={"summary": expected_summary}
    )
    
    result = generate_summary(test_query, test_urls, test_context)
    
    assert result == expected_summary
    
    last_request = requests_mock.last_request
    assert last_request.json() == {
        "query": test_query,
        "focus": test_urls,
        "context": test_context
    }


def test_generate_summary_api_error(mock_env_vars: None, requests_mock: requests_mock.Mocker) -> None:
    """
    Тест обработки ошибки от Perplexity API.
    """
    test_query = "Test query"
    test_urls = ["http://test.com"]
    error_message = "API Error"
    
    requests_mock.post(
        "https://api.perplexity.ai/chat/completions",
        status_code=500,
        json={"error": error_message}
    )
    
    result = generate_summary(test_query, test_urls)
    
    assert result.startswith("Error from Perplexity API")
    assert error_message in result


def test_generate_summary_no_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Тест обработки отсутствующего API ключа.
    """
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)
    
    result = generate_summary("query", ["http://test.com"])
    
    assert result == "Error: PERPLEXITY_API_KEY not set in environment variables" 