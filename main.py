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

from routers.html import (
    exercises as html_exercises,
    programs as html_programs,
    template_exercises as html_template_exercises,
    workout_exercises as html_workout_exercises,
    workout_templates as html_workout_templates,
    workouts as html_workouts,
)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
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
    html_workouts.router
]

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
