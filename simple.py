from prefect import flow, task

@task(log_prints=True)
def my_task(message):
    print(f"Task message: {message}")
    return message

@flow(log_prints=True)
def my_flow(message="Hello, Prefect Cloud!"):
    result = my_task(message)
    print(f"Flow result: {result}")

if __name__ == "__main__":
    my_flow()
