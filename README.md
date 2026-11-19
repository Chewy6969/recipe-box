# Recipe Box API

A FastAPI and SQLite REST API for users and recipes.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn main:app --reload
```

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

- `POST /register` — register a user
- `POST /login` — verify user credentials
- `POST /recipes` — create a recipe
- `GET /recipes` — list recipes (optional `?search=chicken`)
- `GET /recipes/{id}` — get a recipe
- `PUT /recipes/{id}` — replace a recipe
- `DELETE /recipes/{id}` — delete a recipe

The SQLite database is stored in `recipe_box.db` and is created automatically at startup.

Passwords are stored as secure Werkzeug hashes. Recipe endpoints are intentionally
unauthenticated for now; token authentication and ownership checks can be added next.
