import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import (
    exercise_sets,
    exercises,
    muscle_groups,
    muscles,
    program_types,
    programs,
    template_exercises,
    users,
    workout_exercises,
    workout_templates,
    workouts,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(exercise_sets.router)
app.include_router(exercises.router)
app.include_router(muscle_groups.router)
app.include_router(muscles.router)
app.include_router(program_types.router)
app.include_router(programs.router)
app.include_router(template_exercises.router)
app.include_router(users.router)
app.include_router(workout_exercises.router)
app.include_router(workout_templates.router)
app.include_router(workouts.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
