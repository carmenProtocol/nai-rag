from typing import Generator
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Импортируем app после создания моков
@pytest.fixture
def mock_generate_summary() -> Generator[MagicMock, None, None]:
    """
    Фикстура для мокирования сервиса generate_summary.
    """
    with patch("backend.app.api.generate_summary") as mock:
        mock.return_value = "Test summary"
        yield mock


@pytest.fixture
def mock_supabase() -> Generator[None, None, None]:
    """
    Фикстура для мокирования сервиса Supabase.
    """
    with patch("backend.app.api.init_supabase_client") as mock_init:
        with patch("backend.app.api.save_query_log") as mock_save:
            mock_init.return_value = MagicMock()
            mock_save.return_value = None
            yield


@pytest.fixture
def client(mock_generate_summary: MagicMock, mock_supabase: None) -> Generator[TestClient, None, None]:
    """
    Фикстура для создания тестового клиента FastAPI.
    Создаётся после установки моков.
    """
    from backend.app.main import app
    with TestClient(app) as test_client:
        yield test_client


def test_create_query_success(
    client: TestClient,
    mock_generate_summary: MagicMock
) -> None:
    """
    Тест успешного создания запроса через /query endpoint.
    """
    mock_generate_summary.return_value = "Test summary"
    
    response = client.post(
        "/api/query",
        json={
            "query": "Test query",
            "urls": ["http://test.com"]
        }
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code == 200
    assert response.json() == {"summary": "Test summary"}


def test_create_query_with_context_success(
    client: TestClient,
    mock_generate_summary: MagicMock
) -> None:
    """
    Тест успешного создания запроса с контекстом через /query_next endpoint.
    """
    mock_generate_summary.return_value = "Test summary with context"
    
    response = client.post(
        "/api/query_next",
        json={
            "query": "Test query",
            "urls": ["http://test.com"],
            "previous_summary": "Previous context"
        }
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code == 200
    assert response.json() == {"summary": "Test summary with context"}


def test_create_query_validation_error(client: TestClient) -> None:
    """
    Тест валидации входных данных для /query endpoint.
    """
    response = client.post(
        "/api/query",
        json={
            "query": "Test query"
            # Отсутствует обязательное поле urls
        }
    )
    
    assert response.status_code == 422


def test_create_query_perplexity_error(
    client: TestClient,
    mock_generate_summary: MagicMock
) -> None:
    """
    Тест обработки ошибки от Perplexity API.
    """
    error_message = "Test error"
    mock_generate_summary.return_value = f"Error: {error_message}"
    
    response = client.post(
        "/api/query",
        json={
            "query": "Test query",
            "urls": ["http://test.com"]
        }
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code == 500
    assert error_message in response.json()["detail"] 