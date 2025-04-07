import subprocess
from prefect import flow, task
import clickhouse_connect

@task(log_prints=True)
def my_task(message):
    print(f"Task message: {message}")
    return message


@task(log_prints=True)
def extract_new_data():
    """Extracts new or updated data from the source table using clickhouse_connect."""
    client = clickhouse_connect.get_client(
        host='q3zu55b6u5.ap-south-1.aws.clickhouse.cloud',
        user='default',
        password='m.ZYik17aFDmy',
        secure=True
    )
    try:
        query = f"SELECT * FROM test_source"
        result = client.query(query).result()
        print("Result from test_source: ",result)
        return result
    except Exception as e:
        print(f"Error extracting new data: {e}")
        return []
    finally:
        client.close()

@task(log_prints=True)
def insert_clickhouse_data(data):
    print("data received: ",data)
    # data = [tuple(row) for row in data]
    # print("data to insert: ",data)
    # data = [('simple text',)]
    client = clickhouse_connect.get_client(
        host='q3zu55b6u5.ap-south-1.aws.clickhouse.cloud',
        user='default',
        password='m.ZYik17aFDmy',
        secure=True,
    )
    # values = [(item['data'],) for item in data]  # Create a list of tuples
    client.insert("test_destination", data,column_names=["data"])

@flow(log_prints=True)
def my_flow(message="Hello, Prefect Cloud!"):
    subprocess.check_call(["pip", "install", "clickhouse_connect"])
    # result = my_task(message)
    result = extract_new_data()
    insert_clickhouse_data(result)
    print(f"Flow result: {result}")

if __name__ == "__main__":
    my_flow()
