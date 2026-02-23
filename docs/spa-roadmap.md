# SPA Development Roadmap

## Phase 1: Workout Logging (implemented baseline)
- Program selector and template management
- Template exercises ordering and exercise assignment
- Workout creation from templates
- Workout exercise editing (order, notes, exercise)
- Set logging (set number, weight, reps)

## Phase 1 API Refinements
1. Add list endpoint for workout templates (`GET /workout_templates?program_id=`) to reduce route fan-out.
2. Add batch reorder endpoint for template/workout exercises to avoid multiple PUT calls.
3. Return embedded `exercise` objects on workout/template exercise responses to reduce extra lookups.
4. Add pagination and date filters on `GET /programs/{program_id}/workouts`.
5. Validate uniqueness of `set_number` per `workout_exercise_id`.

## Phase 2: Analytics
- Training volume over time (sets x reps x weight)
- Exercise progression trends (e1RM proxies, moving averages)
- Correlations between key compound lift trends
- Program adherence (% planned workouts completed)

## Suggested Near-Term Tasks
1. Break `frontend/src/App.vue` into reusable modules (`TemplateBuilder`, `WorkoutLogger`, `ExerciseSetTable`).
2. Add API integration tests for new/updated routes (`workout_exercises`, `exercise_sets`).
3. Add optimistic UI updates + rollback for reorder operations.
4. Add auth and per-user scoping before production use.
