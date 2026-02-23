from pathlib import Path

from starlette.templating import Jinja2Templates

DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def get_weekday(d):
    if 0 < d <= 7:
        return DAYS[d - 1]
    else:
        return "ERROR"


templates_dir = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))
templates.env.globals["get_weekday"] = get_weekday
