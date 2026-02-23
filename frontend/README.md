# Vue SPA (Phase 1)

## Purpose
Build workout templates and log workouts against this API.

## Setup
```bash
cd frontend
npm install
npm run dev
```

The app reads `VITE_API_BASE_URL`, defaulting to `http://127.0.0.1:8000`.

## Current Features
- Select a program
- Create workout templates per program
- Add/reorder/remove ordered exercises in templates
- Create a workout log from a template
- View workouts by program
- Add/reorder/edit/remove workout exercises
- Add/edit/remove sets (`weight`, `reps`, `set_number`)

## Notes
- Backend CORS is configured for `http://localhost:5173` and `http://127.0.0.1:5173`.
- This UI is intentionally API-first and can be split into smaller components once behavior stabilizes.
