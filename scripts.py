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

# Deploy the flow
def deploy_flow(flow_name: str, task_message: str, work_pool_name: str):
    """Deploys a flow using modern Prefect 2.x approach"""
    # Get absolute path to your script
    script_path = Path(__file__).absolute()

    # Deploy with Docker infrastructure
    dynamic_flow.deploy(
        name=f"{flow_name}-deployment",
        work_pool_name=work_pool_name,
        work_queue_name="default",
        parameters={"message": task_message},
        schedule=IntervalSchedule(interval=timedelta(minutes=1)),
        image="prefecthq/prefect-client:3-latest",
        path=script_path,
    )

# Example usage
deploy_flow(
    flow_name="docker-flow-example",
    task_message="Hello from Docker!",
    work_pool_name="test"  # Must be a Docker-compatible work pool
)
