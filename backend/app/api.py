from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from backend.app.models.requests import UserQuery, UserQueryWithContext
from backend.app.models.responses import SummaryResponse
from backend.app.services.perplexity import generate_summary
from backend.app.services.supabase import init_supabase_client, save_query_log

router = APIRouter()


@router.post("/query", response_model=SummaryResponse)
async def create_query(user_query: UserQuery) -> Dict[str, str]:
    """
    Обрабатывает запрос пользователя и генерирует саммари.

    Args:
        user_query: Запрос пользователя с текстом и URL-адресами.

    Returns:
        SummaryResponse с текстом саммари.

    Raises:
        HTTPException: При ошибках в обработке запроса.
    """
    try:
        # Генерация саммари
        summary = generate_summary(
            query=user_query.query,
            focus_urls=user_query.urls
        )

        if summary.startswith("Error"):
            raise HTTPException(
                status_code=500,
                detail=summary
            )

        # Сохранение в Supabase
        try:
            client = init_supabase_client()
            timestamp = datetime.now(timezone.utc).isoformat()
            save_query_log(
                query=user_query.query,
                response=summary,
                timestamp=timestamp,
                client=client
            )
        except Exception as e:
            # Логируем ошибку Supabase, но продолжаем работу
            print(f"Failed to save to Supabase: {str(e)}")

        return {"summary": summary}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/query_next", response_model=SummaryResponse)
async def create_query_with_context(user_query: UserQueryWithContext) -> Dict[str, str]:
    """
    Обрабатывает запрос пользователя с контекстом и генерирует саммари.

    Args:
        user_query: Запрос пользователя с текстом, URL-адресами и предыдущим контекстом.

    Returns:
        SummaryResponse с текстом саммари.

    Raises:
        HTTPException: При ошибках в обработке запроса.
    """
    try:
        # Генерация саммари с контекстом
        summary = generate_summary(
            query=user_query.query,
            focus_urls=user_query.urls,
            context=user_query.previous_summary
        )

        if summary.startswith("Error"):
            raise HTTPException(
                status_code=500,
                detail=summary
            )

        # Сохранение в Supabase
        try:
            client = init_supabase_client()
            timestamp = datetime.now(timezone.utc).isoformat()
            save_query_log(
                query=user_query.query,
                response=summary,
                timestamp=timestamp,
                client=client
            )
        except Exception as e:
            # Логируем ошибку Supabase, но продолжаем работу
            print(f"Failed to save to Supabase: {str(e)}")

        return {"summary": summary}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        ) 