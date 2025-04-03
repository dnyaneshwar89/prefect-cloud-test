from prefect import flow, deploy
from prefect.runner.storage import GitRepository

# Define your flow
@flow
def my_flow(name):
    print(f"Hello, {name}!")

# Load the flow from a public Git repository
my_flow = flow.from_source(
    source="https://github.com/dnyaneshwar89/prefect-cloud-test.git",  # Replace with your repository URL
    entrypoint="marvinscript.py:my_flow",            # Replace with your file and flow function
)

# Deploy the flow to Prefect Cloud
if __name__ == "__main__":
    deployment = my_flow.deploy(
        flow=my_flow,
        name="example-deployment",
        work_pool_name="test",  # Replace with your work pool name
    )
    print("Deployment created:", deployment)
