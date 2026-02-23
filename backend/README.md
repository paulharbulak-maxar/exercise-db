# Backend

FastAPI backend lives in this directory.

## Run
```bash
cd backend
poetry install
poetry run uvicorn exercise_db.main:app --reload
```

## Tests
```bash
cd backend
poetry run python -m pytest
```
