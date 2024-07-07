from sanic import Sanic, response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

# Create a new Sanic app
app = Sanic(name="HelloWorldApp")


# Endpoint to return "Hello World" at the root URL
@app.route("/")
async def hello_world(request):
    return response.text("Hello World!")


# Schedule a function to run once, 30 seconds from server start
def schedule_hello():
    print("Hello")


# Setup APScheduler
def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(schedule_hello, 'date', run_date=datetime.now() + timedelta(seconds=30))
    scheduler.start()


# Before the server starts, set up the scheduler
@app.before_server_start
async def initialize_scheduler(app, loop):
    setup_scheduler()


# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
