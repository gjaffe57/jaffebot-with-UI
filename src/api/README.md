# JaffeBot 3.0 API

This is the FastAPI backend for JaffeBot 3.0.

## Endpoints

- `POST /token` — Obtain OAuth2 token (dummy, returns a static token)
- `GET /health` — Health check
- `GET /agents` — List agents (placeholder)
- `GET /audits` — List audits (placeholder)
- `GET /content` — List content (placeholder)
- `GET /backlinks` — List backlinks (placeholder)
- `GET /settings` — Get settings (requires Bearer token)

## Running the API

1. Install dependencies (if not already):
   ```sh
   poetry install
   ```
2. Start the server:
   ```sh
   poetry run uvicorn main:app --reload
   ```

The API will be available at http://localhost:8000

## Testing Authentication

1. Obtain a token:
   ```sh
   curl -X POST http://localhost:8000/token
   # Response: {"access_token": "secrettoken", "token_type": "bearer"}
   ```
2. Access a protected endpoint:
   ```sh
   curl -H "Authorization: Bearer secrettoken" http://localhost:8000/settings
   ```

## CORS

CORS is enabled for http://localhost:3000 (Next.js dashboard). 