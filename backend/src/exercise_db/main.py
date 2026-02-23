from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from exercise_db.routers import (
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
from exercise_db.routers.html import exercises as html_exercises
from exercise_db.routers.html import programs as html_programs
from exercise_db.routers.html import template_exercises as html_template_exercises
from exercise_db.routers.html import workout_exercises as html_workout_exercises
from exercise_db.routers.html import workout_templates as html_workout_templates
from exercise_db.routers.html import workouts as html_workouts

app = FastAPI()
package_root = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(package_root / "static")), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    exercise_sets.router,
    exercises.router,
    program_types.router,
    programs.router,
    muscle_groups.router,
    muscles.router,
    program_types.router,
    template_exercises.router,
    users.router,
    workout_exercises.router,
    workout_templates.router,
    workouts.router,
    html_exercises.router,
    html_programs.router,
    html_template_exercises.router,
    html_workout_exercises.router,
    html_workout_templates.router,
    html_workouts.router,
]

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
