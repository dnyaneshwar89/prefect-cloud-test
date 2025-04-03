
PREFECT_CLOUD_URL = "https://api.prefect.cloud/api/accounts/db1dc987-94b8-427d-8c8d-2ff3441e3ab6/workspaces/287373fb-cd00-4ad7-9654-97b9245253ba"
PREFECT_API_KEY = "pnu_PhJBthw7cWsq4oK9kEpKvoJRaQcKJh0a5onE"  # Store securely
PREFECT_WORK_POOL = "test"  # Your work pool name


import asyncio
import requests
import os

from prefect import flow
from prefect.client.schemas.schedules import IntervalSchedule
from prefect.filesystems import RemoteFileSystem

from datetime import timedelta

from prefect_github import GitHubRepository

# Prefect Cloud API details
ACCOUNT_ID = "your_account_id"  # Replace with actual account ID
WORKSPACE_ID = "your_workspace_id"  # Replace with actual workspace ID
# PREFECT_CLOUD_URL = f"https://api.prefect.cloud/api/accounts/{ACCOUNT_ID}/workspaces/{WORKSPACE_ID}"
# PREFECT_API_KEY = "your-prefect-api-key"  # Store securely, e.g., in environment variables
# PREFECT_WORK_POOL = "test"  # Your work pool name

headers = {
    "Authorization": f"Bearer {PREFECT_API_KEY}",
    "Content-Type": "application/json"
}
# Store flow code in Prefect Cloud storage
# storage = RemoteFileSystem(basepath="prefect://")
#
github_block = GitHubRepository(
    repository_url="dnyaneshwar89/prefect-cloud-test",
    reference="main"
)

# Save the block for future use
github_block.save("github-private-storage", overwrite=True)


@flow
def etl_flow(company_id: str):
    print(f"Running ETL for company {company_id}")

async def create_and_trigger_deployment(company_id: str):
    deployment_name = f"etl-flow-company-{company_id}"

    # Create deployment using the new Prefect method
    deployment = await etl_flow.deploy(
        name=deployment_name,
        work_pool_name=PREFECT_WORK_POOL,
        parameters={"company_id": company_id},
        schedule=IntervalSchedule(interval=timedelta(minutes=1)),
        image="prefecthq/prefect-client:3-latest"
        # image="prefecthq/prefect-client:3-latest"
        # storage=github_block  
    )

    print(f"Deployment {deployment_name} created successfully.")

    # Fetch deployment ID
    deployment_id = get_deployment_id(deployment_name)
    if deployment_id:
        trigger_response = trigger_deployment(deployment_id)
        print("Deployment triggered:", trigger_response)
    else:
        print("Deployment not found.")

def get_deployment_id(deployment_name):
    """Fetch deployment ID from Prefect Cloud"""
    url = f"{PREFECT_CLOUD_URL}/deployments/"
    response = requests.get(url, headers=headers)
    
    try:
        deployments = response.json().get("data", [])  # Ensure we get the list of deployments
        for deployment in deployments:
            if deployment.get("name") == deployment_name:
                return deployment.get("id")
    except Exception as e:
        print(f"Error fetching deployments: {e}")
    
    return None

def trigger_deployment(deployment_id):
    """Trigger deployment using Prefect Cloud API"""
    url = f"{PREFECT_CLOUD_URL}/deployments/{deployment_id}/create_flow_run"
    response = requests.post(url, headers=headers)
    return response.json()

def trigger_flow(company_id: str):
    """Trigger ETL flow dynamically via API"""
    
    # Directly run the flow without creating a deployment
    etl_flow.serve(name=f"etl-flow-{company_id}", parameters={"company_id": company_id})

    print(f"Triggered ETL flow for company {company_id}")

# if __name__ == "__main__":
    # company_id = "12345"  # Replace with actual company ID
    # trigger_flow(company_id)

if __name__ == "__main__":
    company_id = "12345"  # Replace with actual company ID
    asyncio.run(create_and_trigger_deployment(company_id))
