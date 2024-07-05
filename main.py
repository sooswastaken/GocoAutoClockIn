from pytz import timezone
from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
import json
from utils import click_punch  # USE THIS
from sanic.exceptions import NotFound

app = Sanic("AutoClockInApp")
scheduler = AsyncIOScheduler()


# Load configuration
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        data = {
            "monday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "tuesday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "wednesday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "thursday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "friday": {"enabled": True, "start": "09:00", "end": "13:00"},
        }

        # save the default configuration
        with open("config.json", "w") as f:
            json.dump(data, f, indent=2)
        return data


config = load_config()


# Save configuration
def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)


eastern = timezone('US/Eastern')


def schedule_jobs():
    scheduler.remove_all_jobs()
    local_tz = datetime.now().astimezone().tzinfo  # Get server's local timezone

    for day, settings in config.items():
        if settings["enabled"]:
            start_time_est = datetime.strptime(settings["start"], '%H:%M').replace(tzinfo=eastern)
            end_time_est = datetime.strptime(settings["end"], '%H:%M').replace(tzinfo=eastern)

            # Convert EST to local time
            start_time_local = start_time_est.astimezone(local_tz)
            end_time_local = end_time_est.astimezone(local_tz)

            scheduler.add_job(clock_in, 'cron', day_of_week=day[:3],
                              hour=start_time_local.hour, minute=start_time_local.minute)
            scheduler.add_job(clock_out, 'cron', day_of_week=day[:3],
                              hour=end_time_local.hour, minute=end_time_local.minute)


@app.listener('before_server_start')
async def setup_scheduler(_, __):
    scheduler.start()
    schedule_jobs()


@app.route("/update", methods=["POST"])
async def update(request):
    global config
    config = request.json
    save_config()
    schedule_jobs()
    return response.json({"status": "success"})


@app.route("/get-config")
async def get_config(_):
    return response.json(config)


@app.route("/test", methods=["POST"])
async def test_punch(_):
    click_punch(test=True)
    return response.json({"status": "success"})


@app.route("/")
async def index(_):
    return await response.file("./frontend/dist/index.html")


# serve /frontend/dist folder on /
app.static("/", "./frontend/dist")


# serve /frontend/dist/index.html for 404
@app.exception(NotFound)
async def ignore_404s(request, exception):
    return await response.file("./frontend/dist/index.html")


async def clock_in():
    print("Clocking in...")
    click_punch()


async def clock_out():
    print("Clocking out...")
    click_punch()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
