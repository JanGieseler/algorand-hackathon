# API Server

FastAPI backend service for the Algorand hackathon project.

## Development

```bash
# Install dependencies
poetry install

# Start development server
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

The API will be available at http://localhost:8000

- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc