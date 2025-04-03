
from prefect import flow, task
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta
from pathlib import Path

# Define your flow
@task
def my_task(message):
    print(f"Task message: {message}")
    return message

@flow(name="dynamic-flow")  # Name is required for deployment
def dynamic_flow(message: str):
    result = my_task(message)
    print(f"Flow result: {result}")
