# nAI RAG API

FastAPI backend for generating summaries using Perplexity API with RAG (Retrieval-Augmented Generation) approach.

## Features

- Text summarization using Perplexity API
- Context-aware summarization with previous summaries
- Supabase integration for query logging
- Full test coverage
- Ready for Vercel deployment

## API Endpoints

- `/api/query` - Generate summary from URLs
- `/api/query_next` - Generate summary with context from previous summary
- `/api/docs` - Swagger documentation

## Setup

1. Clone the repository:
```bash
git clone https://github.com/carmenProtocol/nai-rag.git
cd nai-rag
```

2. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# PERPLEXITY_API_KEY=your_key
# SUPABASE_URL=your_url
# SUPABASE_API_KEY=your_key
```

4. Run tests:
```bash
python3 -m pytest
```

5. Run development server:
```bash
uvicorn backend.app.main:app --reload
```

## Deployment

The project is configured for deployment on Vercel:

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Set environment variables in Vercel dashboard.

## Project Structure

```
backend/
├── app/
│   ├── models/      # Pydantic models
│   ├── services/    # External services integration
│   ├── api.py       # API routes
│   └── main.py      # FastAPI application
└── tests/           # Test files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT 