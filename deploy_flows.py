
from prefect import flow, task
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta
from flows.my_flows import dynamic_flow

# Deploy the flow
def deploy_flow(flow_name: str, task_message: str, work_pool_name: str):
    """Deploys a flow using modern Prefect 2.x approach"""
    # Get absolute path to your script

    # Deploy with Docker infrastructure
    dynamic_flow.deploy(
        name=f"{flow_name}-deployment",
        work_pool_name=work_pool_name,
        work_queue_name="default",
        parameters={"message": task_message},
        schedule=IntervalSchedule(interval=timedelta(minutes=1)),
        image="prefecthq/prefect-client:3-latest",
    )

if __name__ == "__main__":
    # Example usage
    deploy_flow(
        flow_name="docker-flow-example",
        task_message="Hello from Docker!",
        work_pool_name="test"  # Must be a Docker-compatible work pool
    )

