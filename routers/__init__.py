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
    if d > 0 and d <= 7:
        return DAYS[d - 1]
    else:
        return "ERROR"


templates = Jinja2Templates(directory="templates/")
templates.env.globals["get_weekday"] = get_weekday
