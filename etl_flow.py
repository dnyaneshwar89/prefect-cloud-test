
from prefect import flow

@flow
def etl_flow(company_id: str):
    print(f"Running ETL for company {company_id}")
