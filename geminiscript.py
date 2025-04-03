from prefect import flow, task
from prefect.client.schemas.schedules import IntervalSchedule
from datetime import timedelta
from prefect_git import GitHub

# Define your flow
@task
def my_task(message):
    print(f"Task message: {message}")
    return message

@flow
def dynamic_flow(message):
    result = my_task(message)
    print(f"Flow result: {result}")

# Deploy the flow from git
def deploy_flow_from_git(flow_name, task_message, work_pool_name, git_block_name, flow_file_path):
    """Deploys a flow from a Git repository to Prefect Cloud."""

    # Load the Git block
    git_block = GitHub.load(git_block_name)

    # Deploy the flow
    dynamic_flow.deploy(
        name=f"{flow_name}-deployment",
        work_pool_name=work_pool_name,
        parameters={"message": task_message},
        schedule=IntervalSchedule(interval=timedelta(minutes=1)),
        build=dict(git=git_block), # use the git block inside the build parameter.
        path=flow_file_path,  # Path to the flow file in the repository
        entrypoint="geminiscript.py.py:dynamic_flow", # entrypoint to the flow.
        push=False,
    )

# Example usage
flow_name = "dynamic_flow_from_git"
task_message = "Hello from Git!"
work_pool_name = "test"
git_block_name = "https://github.com/dnyaneshwar89/prefect-cloud-test.git" # Name of your Git block
flow_file_path = "geminiscript.py" # The path to the python file within the repository.

deploy_flow_from_git(flow_name, task_message, work_pool_name, git_block_name, flow_file_path)
