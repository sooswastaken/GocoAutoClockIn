import json
import random

from sanic import Sanic, response
from sanic.exceptions import NotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from utils import click_punch

app = Sanic("AutoClockInApp")

# Create the scheduler outside to be available globally
scheduler = AsyncIOScheduler()


# Load and save configuration
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "sunday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "monday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "tuesday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "wednesday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "thursday": {"enabled": True, "start": "08:35", "end": "17:30"},
            "friday": {"enabled": True, "start": "09:00", "end": "13:00"}
        }
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=2)
        return default_config


def save_config(_config):
    with open("config.json", "w") as f:
        json.dump(_config, f, indent=2)


config = load_config()


@app.listener('before_server_start')
async def setup_scheduler(app, loop):
    scheduler.start()
    schedule_jobs()


def schedule_jobs():
    scheduler.remove_all_jobs()
    for day, settings in config.items():
        if settings['enabled']:
            # Calculate random offsets for start and end times
            start_offset = timedelta(minutes=random.randint(-3, 3))
            end_offset = timedelta(minutes=random.randint(-3, 3))

            # Calculate actual start and end times with offsets
            start_time = datetime.strptime(settings['start'], "%H:%M") + start_offset
            end_time = datetime.strptime(settings['end'], "%H:%M") + end_offset

            # Schedule start job with random offset
            scheduler.add_job(
                click_punch,
                trigger='cron',
                day_of_week=day[:3],
                hour=start_time.hour,
                minute=start_time.minute,
                args=[False]
            )

            # Schedule end job with random offset
            scheduler.add_job(
                click_punch,
                trigger='cron',
                day_of_week=day[:3],
                hour=end_time.hour,
                minute=end_time.minute,
                args=[True]
            )


@app.route("/update", methods=["POST"])
async def update(request):
    global config
    config = request.json
    save_config(config)
    schedule_jobs()
    return response.json({"status": "success"})


@app.route("/get-scheduled-jobs")
async def get_scheduled_jobs(request):
    jobs = scheduler.get_jobs()
    return response.text("\n".join([f"{job.trigger}: {job.func}" for job in jobs]))


@app.route("/get-config")
async def get_config(request):
    return response.json(config)


@app.route("/test", methods=["POST"])
async def test_punch(request):
    click_punch(test=True)
    return response.json({"status": "success"})


@app.route("/")
async def index(request):
    return await response.file("./frontend/dist/index.html")


app.static("/", "./frontend/dist")


@app.exception(NotFound)
async def ignore_404s(request, exception):
    return await response.file("./frontend/dist/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
