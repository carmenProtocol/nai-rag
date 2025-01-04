from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import router

# Инициализация приложения
app = FastAPI(
    title="Summary API",
    description="API для генерации саммари с использованием Perplexity API",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "https://your-frontend-domain.vercel.app"  # Замените на ваш домен
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(router, prefix="/api") 